#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_ARG="${1:-$PWD}"

[[ -d "$TARGET_ARG" && ! -L "$TARGET_ARG" ]] || { echo "Target directory must be a real directory: $TARGET_ARG" >&2; exit 1; }
TARGET_DIR="$(cd "$TARGET_ARG" && pwd -P)"
SOURCE_DIR="$(cd "$SOURCE_DIR" && pwd -P)"

if [[ "$TARGET_DIR" == "$SOURCE_DIR" || "$TARGET_DIR" == "$SOURCE_DIR"/* ]]; then
  echo "Target directory must not be the installer repository or one of its children: $TARGET_DIR" >&2
  exit 2
fi

source_directories=(
  ".codex"
  ".codex/agents"
  ".agents"
  ".agents/skills"
  ".codex-evals"
  "scripts"
  "tests"
  ".github"
  ".github/workflows"
  "docs"
  "docs/agent"
  "docs/exec-plans"
  "docs/exec-plans/active"
  "docs/exec-plans/completed"
)
source_files=(
  "AGENTS.md"
  ".codex/config.toml"
  ".codex-evals/README.md"
  ".codex-evals/runs.jsonl"
  "docs/agent/README.md"
  ".github/workflows/harness-check.yml"
  "scripts/check-harness.py"
  "scripts/eval-report.py"
  "scripts/eval_schema.py"
  "scripts/secure_install.py"
  "tests/test_harness.py"
)
source_agents=(
  "product-analyst"
  "system-analyst"
  "researcher"
  "implementer"
  "worker"
  "test-engineer"
  "reviewer"
  "requirements-reviewer"
  "security-reviewer"
  "architect"
  "oracle"
)
source_skills=(
  "bootstrap-project"
  "debug"
  "plan"
  "verify"
  "review-loop"
  "improve-harness"
  "docs-gardening"
  "record-outcome"
  "evaluate-harness"
)
for relative_path in "${source_directories[@]}"; do
  if [[ ! -d "$SOURCE_DIR/$relative_path" || -L "$SOURCE_DIR/$relative_path" ]]; then
    echo "Installer source is incomplete: expected directory $relative_path" >&2
    exit 1
  fi
done

for source_tree in ".codex" ".agents" ".codex-evals"; do
  if [[ -n "$(find "$SOURCE_DIR/$source_tree" -type l -print -quit)" ]]; then
    echo "Installer source contains a symlink inside $source_tree" >&2
    exit 1
  fi
done
for relative_path in "${source_files[@]}"; do
  if [[ ! -f "$SOURCE_DIR/$relative_path" || -L "$SOURCE_DIR/$relative_path" ]]; then
    echo "Installer source is incomplete: expected file $relative_path" >&2
    exit 1
  fi
done
for agent in "${source_agents[@]}"; do
  relative_path=".codex/agents/$agent.toml"
  if [[ ! -f "$SOURCE_DIR/$relative_path" || -L "$SOURCE_DIR/$relative_path" ]]; then
    echo "Installer source is incomplete: expected file $relative_path" >&2
    exit 1
  fi
done
for skill in "${source_skills[@]}"; do
  relative_path=".agents/skills/$skill/SKILL.md"
  if [[ ! -f "$SOURCE_DIR/$relative_path" || -L "$SOURCE_DIR/$relative_path" ]]; then
    echo "Installer source is incomplete: expected file $relative_path" >&2
    exit 1
  fi
done

conflicts=(
  "AGENTS.md"
  ".codex/config.toml"
  ".codex-evals/README.md"
  ".codex-evals/runs.jsonl"
  "docs/exec-plans/active/.gitkeep"
  "docs/exec-plans/completed/.gitkeep"
  ".github/workflows/harness-check.yml"
  "scripts/check-harness.py"
  "scripts/eval-report.py"
  "scripts/eval_schema.py"
  "tests/test_harness.py"
)
for agent in "${source_agents[@]}"; do
  conflicts+=(".codex/agents/$agent.toml")
done
for skill in "${source_skills[@]}"; do
  conflicts+=(".agents/skills/$skill/SKILL.md")
done

for relative_path in "${conflicts[@]}"; do
  if [[ -e "$TARGET_DIR/$relative_path" || -L "$TARGET_DIR/$relative_path" ]]; then
    echo "Refusing to overwrite existing $relative_path in: $TARGET_DIR" >&2
    echo "Merge deliberately so existing project instructions and validation are preserved." >&2
    exit 2
  fi
done

directory_parents=(
  ".codex"
  ".codex/agents"
  ".agents"
  ".agents/skills"
  ".codex-evals"
  "scripts"
  "tests"
  ".github"
  ".github/workflows"
  "docs"
  "docs/agent"
  "docs/exec-plans"
  "docs/exec-plans/active"
  "docs/exec-plans/completed"
)
for relative_path in "${directory_parents[@]}"; do
  if [[ ( -e "$TARGET_DIR/$relative_path" || -L "$TARGET_DIR/$relative_path" ) && ( ! -d "$TARGET_DIR/$relative_path" || -L "$TARGET_DIR/$relative_path" ) ]]; then
    echo "Refusing to install because $relative_path is not a directory: $TARGET_DIR/$relative_path" >&2
    exit 2
  fi
done

existing_agent_readme="$TARGET_DIR/docs/agent/README.md"
if [[ -L "$existing_agent_readme" || ( -e "$existing_agent_readme" && ! -f "$existing_agent_readme" ) ]]; then
  echo "Refusing to install because docs/agent/README.md is not a regular file: $existing_agent_readme" >&2
  exit 2
fi

python3 "$SOURCE_DIR/scripts/secure_install.py" "$SOURCE_DIR" "$TARGET_DIR"

echo "Installed Codex workflow into: $TARGET_DIR"
echo "Next: trust/open the project in Codex and run bootstrap-project if repository knowledge is not already legible."
