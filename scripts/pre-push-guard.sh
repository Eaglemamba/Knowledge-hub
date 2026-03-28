#!/usr/bin/env bash
# pre-push-guard.sh
# Blocks git push --force commands. Called from PreToolUse hook.

cmd=$(jq -r '.tool_input.command // ""')
if echo "$cmd" | grep -qE 'git push.*(--force|-f)'; then
  printf '{"continue":false,"stopReason":"Force push blocked — remove --force/-f, or run manually to confirm."}'
  exit 2
fi
