#!/bin/bash
# Claude Code global config sync setup
# Run once on each machine after cloning knowledge-hub
# Safe: preserves existing project-local .claude/ configs

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "=== Claude Code Config Sync Setup ==="
echo "Source: $SCRIPT_DIR"
echo "Target: $CLAUDE_DIR"
echo ""

# Ensure ~/.claude exists
mkdir -p "$CLAUDE_DIR"

# --- settings.json ---
if [ -L "$CLAUDE_DIR/settings.json" ]; then
    echo "[skip] settings.json already symlinked"
elif [ -f "$CLAUDE_DIR/settings.json" ]; then
    echo "[backup] settings.json -> settings.json.bak"
    mv "$CLAUDE_DIR/settings.json" "$CLAUDE_DIR/settings.json.bak"
    ln -sf "$SCRIPT_DIR/settings.json" "$CLAUDE_DIR/settings.json"
    echo "[link] settings.json"
else
    ln -sf "$SCRIPT_DIR/settings.json" "$CLAUDE_DIR/settings.json"
    echo "[link] settings.json"
fi

# --- Global commands ---
mkdir -p "$CLAUDE_DIR/commands"
for f in "$SCRIPT_DIR/commands/"*.md; do
    [ -f "$f" ] || continue
    name=$(basename "$f")
    if [ -L "$CLAUDE_DIR/commands/$name" ]; then
        echo "[skip] commands/$name already symlinked"
    else
        [ -f "$CLAUDE_DIR/commands/$name" ] && mv "$CLAUDE_DIR/commands/$name" "$CLAUDE_DIR/commands/${name}.bak"
        ln -sf "$f" "$CLAUDE_DIR/commands/$name"
        echo "[link] commands/$name"
    fi
done

# --- Global skills (directory-based) ---
mkdir -p "$CLAUDE_DIR/skills"
for d in "$SCRIPT_DIR/skills/"/*/; do
    [ -d "$d" ] || continue
    name=$(basename "$d")
    if [ -L "$CLAUDE_DIR/skills/$name" ]; then
        echo "[skip] skills/$name already symlinked"
    else
        [ -d "$CLAUDE_DIR/skills/$name" ] && mv "$CLAUDE_DIR/skills/$name" "$CLAUDE_DIR/skills/${name}.bak"
        ln -sf "$d" "$CLAUDE_DIR/skills/$name"
        echo "[link] skills/$name"
    fi
done

echo ""
echo "Done. Existing project-local .claude/ configs in repos are untouched."
echo "To sync updates: git pull in knowledge-hub -- symlinks auto-resolve."
