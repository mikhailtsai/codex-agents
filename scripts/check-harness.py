#!/usr/bin/env python3
from pathlib import Path
import json
import sys
import tomllib

try:
    from eval_schema import validate_row
except ImportError as error:
    print("Harness check FAILED")
    print(f"- scripts/eval_schema.py: cannot import shared schema: {error}")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
errors = []

def fail(msg): errors.append(msg)

# Parse all TOML shipped to Codex.
toml_paths = [ROOT / ".codex/config.toml", *sorted((ROOT / ".codex/agents").glob("*.toml"))]
toml_data = {}
for path in toml_paths:
    try:
        with path.open("rb") as f: toml_data[path] = tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError) as e:
        fail(f"{path.relative_to(ROOT)}: invalid TOML: {e}")

agent_paths = sorted((ROOT / ".codex/agents").glob("*.toml"))
agents = {p.stem for p in agent_paths}
skills = {p.parent.name for p in (ROOT / ".agents/skills").glob("*/SKILL.md")}
expected_agents = {
    "product-analyst",
    "system-analyst",
    "researcher",
    "implementer",
    "worker",
    "test-engineer",
    "reviewer",
    "requirements-reviewer",
    "security-reviewer",
    "architect",
    "oracle",
}
for name in sorted(expected_agents - agents):
    fail(f".codex/agents/{name}.toml: required agent is missing")

# Validate the project-level configuration and each agent's runtime contract.
config = toml_data.get(ROOT / ".codex/config.toml", {})
agent_config = config.get("agents", {})
if agent_config.get("enabled") is not True:
    fail(".codex/config.toml: [agents].enabled must be true")
if type(agent_config.get("max_concurrent_threads_per_session")) is not int or agent_config["max_concurrent_threads_per_session"] < 1:
    fail(".codex/config.toml: [agents].max_concurrent_threads_per_session must be a positive integer")
if agent_config.get("default_subagent_model") != "gpt-5.6-luna":
    fail(".codex/config.toml: [agents].default_subagent_model must be gpt-5.6-luna")
if config.get("model") != "gpt-5.6-luna":
    fail(".codex/config.toml: model must default to gpt-5.6-luna")
if config.get("model_reasoning_effort") != "high":
    fail(".codex/config.toml: model_reasoning_effort must default to high")

required_agent_fields = {"name", "description", "model", "model_reasoning_effort", "sandbox_mode", "developer_instructions"}
allowed_sandboxes = {"read-only", "workspace-write", "danger-full-access"}
seen_agent_names = set()
for path in agent_paths:
    data = toml_data.get(path)
    if not data:
        continue
    missing = required_agent_fields - data.keys()
    for field in sorted(missing):
        fail(f"{path.relative_to(ROOT)}: missing required field {field!r}")
    name = data.get("name")
    if name != path.stem:
        fail(f"{path.relative_to(ROOT)}: name must match filename stem {path.stem!r}")
    if name in seen_agent_names:
        fail(f"{path.relative_to(ROOT)}: duplicate agent name {name!r}")
    seen_agent_names.add(name)
    if data.get("sandbox_mode") not in allowed_sandboxes:
        fail(f"{path.relative_to(ROOT)}: unsupported sandbox_mode {data.get('sandbox_mode')!r}")

# Every skill must have minimal YAML-like frontmatter understood by Codex.
for path in (ROOT / ".agents/skills").glob("*/SKILL.md"):
    try:
        text = path.read_text()
    except OSError as e:
        fail(f"{path.relative_to(ROOT)}: cannot read skill: {e}")
        continue
    frontmatter = text.split("---\n", 2)
    if len(frontmatter) < 3 or not frontmatter[0] == "":
        fail(f"{path.relative_to(ROOT)}: missing name/description frontmatter")
        continue
    fields = {}
    for line in frontmatter[1].splitlines():
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip()
    if not fields.get("name") or not fields.get("description"):
        fail(f"{path.relative_to(ROOT)}: missing name/description frontmatter")
    if fields.get("name") != path.parent.name:
        fail(f"{path.relative_to(ROOT)}: frontmatter name must match directory name")

# Explicit backtick references in AGENTS.md must resolve when they name a known role/skill.
try:
    policy = (ROOT / "AGENTS.md").read_text()
except OSError as error:
    fail(f"AGENTS.md: cannot read file: {error}")
    policy = ""
for name in sorted(expected_agents & agents):
    if f"`{name}`" not in policy:
        fail(f"AGENTS.md: shipped agent '{name}' is not discoverable")

# Known workflow references must exist.
for name in ["bootstrap-project","debug","plan","verify","review-loop","improve-harness","record-outcome","evaluate-harness"]:
    if name not in skills:
        fail(f"AGENTS.md workflow requires missing skill: {name}")

# Model policy is intentionally enforceable: routine roles stay on Luna.
for path in agent_paths:
    data = toml_data.get(path, {})
    model = data.get("model")
    if path.stem not in {"architect","oracle"} and model != "gpt-5.6-luna":
        fail(f"{path.relative_to(ROOT)}: routine role must use gpt-5.6-luna, got {model!r}")
    if path.stem == "architect" and model != "gpt-5.6-terra":
        fail(f"{path.relative_to(ROOT)}: architect must use gpt-5.6-terra, got {model!r}")
    if path.stem == "oracle" and model != "gpt-5.6-sol":
        fail(f"{path.relative_to(ROOT)}: oracle must use gpt-5.6-sol, got {model!r}")

# Eval layer must exist and its journal must remain valid JSONL.
for rel in [
    "AGENTS.md",
    ".codex-evals/README.md",
    ".codex-evals/runs.jsonl",
    "scripts/eval-report.py",
    "scripts/eval_schema.py",
    ".github/workflows/harness-check.yml",
    "tests/test_harness.py",
]:
    if not (ROOT / rel).exists():
        fail(f"missing evaluation artifact: {rel}")
for rel in [
    ".codex",
    ".agents",
    ".codex-evals",
    "docs/exec-plans/active",
    "docs/exec-plans/completed",
]:
    if not (ROOT / rel).is_dir():
        fail(f"missing harness directory: {rel}")

journal = ROOT / ".codex-evals/runs.jsonl"
if journal.exists() and not journal.is_file():
    fail(".codex-evals/runs.jsonl: expected a regular file")
elif journal.is_file():
    for n, line in enumerate(journal.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except Exception as e:
            fail(f".codex-evals/runs.jsonl line {n}: invalid JSON: {e}")
            continue
        errors.extend(f".codex-evals/runs.jsonl {error}" for error in validate_row(row, n, agents))

if errors:
    print("Harness check FAILED")
    for e in errors: print(f"- {e}")
    sys.exit(1)
print(f"Harness check PASS: {len(agents)} agents, {len(skills)} skills")
