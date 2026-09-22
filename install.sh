#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-$PWD}"

[[ -d "$TARGET_DIR" ]] || { echo "Target directory does not exist: $TARGET_DIR" >&2; exit 1; }

if [[ -e "$TARGET_DIR/.codex" || -e "$TARGET_DIR/.agents" || -e "$TARGET_DIR/.codex-evals" || -e "$TARGET_DIR/AGENTS.md" ]]; then
  echo "Refusing to overwrite existing .codex, .agents, .codex-evals, or AGENTS.md in: $TARGET_DIR" >&2
  echo "Merge deliberately so existing project instructions and skills are preserved." >&2
  exit 2
fi

cp -R "$SOURCE_DIR/.codex" "$TARGET_DIR/.codex"
cp -R "$SOURCE_DIR/.agents" "$TARGET_DIR/.agents"
cp "$SOURCE_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
cp -R "$SOURCE_DIR/.codex-evals" "$TARGET_DIR/.codex-evals"
mkdir -p "$TARGET_DIR/scripts"
cp "$SOURCE_DIR/scripts/eval-report.py" "$TARGET_DIR/scripts/eval-report.py"

mkdir -p "$TARGET_DIR/docs/agent" "$TARGET_DIR/docs/exec-plans/active" "$TARGET_DIR/docs/exec-plans/completed"
if [[ ! -e "$TARGET_DIR/docs/agent/README.md" ]]; then
  cp "$SOURCE_DIR/docs/agent/README.md" "$TARGET_DIR/docs/agent/README.md"
fi

echo "Installed Codex workflow into: $TARGET_DIR"
echo "Next: trust/open the project in Codex and run bootstrap-project if repository knowledge is not already legible."
