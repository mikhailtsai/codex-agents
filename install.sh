#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-$PWD}"

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Target directory does not exist: $TARGET_DIR" >&2
  exit 1
fi

if [[ -e "$TARGET_DIR/.codex" || -e "$TARGET_DIR/AGENTS.md" ]]; then
  echo "Refusing to overwrite existing .codex or AGENTS.md in: $TARGET_DIR" >&2
  echo "Merge them deliberately so existing project instructions are preserved." >&2
  exit 2
fi

cp -R "$SOURCE_DIR/.codex" "$TARGET_DIR/.codex"
cp "$SOURCE_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"

# Knowledge/plan directories are additive. Never overwrite existing project docs.
mkdir -p "$TARGET_DIR/docs/agent" "$TARGET_DIR/docs/exec-plans/active" "$TARGET_DIR/docs/exec-plans/completed"
if [[ ! -e "$TARGET_DIR/docs/agent/README.md" ]]; then
  cp "$SOURCE_DIR/docs/agent/README.md" "$TARGET_DIR/docs/agent/README.md"
fi

echo "Installed Codex workflow into: $TARGET_DIR"
echo "Next: start Codex and run the bootstrap-project skill if project knowledge is not already legible."
