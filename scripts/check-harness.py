#!/usr/bin/env python3
from pathlib import Path
import re, sys, tomllib

ROOT = Path(__file__).resolve().parents[1]
errors = []

def fail(msg): errors.append(msg)

# Parse all TOML shipped to Codex.
for path in [ROOT / ".codex/config.toml", *sorted((ROOT / ".codex/agents").glob("*.toml"))]:
    try:
        with path.open("rb") as f: tomllib.load(f)
    except Exception as e:
        fail(f"{path.relative_to(ROOT)}: invalid TOML: {e}")

agents = {p.stem for p in (ROOT / ".codex/agents").glob("*.toml")}
skills = {p.parent.name for p in (ROOT / ".agents/skills").glob("*/SKILL.md")}

# Every skill must have minimal YAML-like frontmatter understood by Codex.
for path in (ROOT / ".agents/skills").glob("*/SKILL.md"):
    text = path.read_text()
    if not text.startswith("---\n") or "\nname:" not in text or "\ndescription:" not in text:
        fail(f"{path.relative_to(ROOT)}: missing name/description frontmatter")

# Explicit backtick references in AGENTS.md must resolve when they name a known role/skill.
policy = (ROOT / "AGENTS.md").read_text()
for name in sorted(agents):
    if f"`{name}`" not in policy:
        fail(f"AGENTS.md: shipped agent '{name}' is not discoverable")

# Known workflow references must exist.
for name in ["bootstrap-project","debug","plan","verify","review-loop","improve-harness"]:
    if name not in skills:
        fail(f"AGENTS.md workflow requires missing skill: {name}")

# Model policy is intentionally enforceable: routine roles stay on Luna.
for path in (ROOT / ".codex/agents").glob("*.toml"):
    with path.open("rb") as f: data = tomllib.load(f)
    model = data.get("model")
    if path.stem not in {"architect","oracle"} and model != "gpt-5.6-luna":
        fail(f"{path.relative_to(ROOT)}: routine role must use gpt-5.6-luna, got {model!r}")

if errors:
    print("Harness check FAILED")
    for e in errors: print(f"- {e}")
    sys.exit(1)
print(f"Harness check PASS: {len(agents)} agents, {len(skills)} skills")
