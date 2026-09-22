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
  echo "Merge them manually so existing project instructions are not lost." >&2
  exit 2
fi

cp -R "$SOURCE_DIR/.codex" "$TARGET_DIR/.codex"
cp "$SOURCE_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"

echo "Installed Codex agent harness into: $TARGET_DIR"
echo "Start Codex normally from that repository."
