#!/usr/bin/env bash
# post-push-health.sh
# Regenerates health dashboard after push in health-check repos.

jq -r '.tool_input.command // ""' | {
  read -r cmd
  cwd=$(pwd)
  if echo "$cwd" | grep -qi 'health-check'; then
    if [ -f scripts/generate_dashboard.py ]; then
      python3 scripts/generate_dashboard.py 2>/dev/null
      if [[ "$OSTYPE" == "darwin"* ]]; then
        open reviews/health_dashboard.png 2>/dev/null
      elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]] || grep -qi microsoft /proc/version 2>/dev/null; then
        cmd.exe /c start "" "reviews\\health_dashboard.png" 2>/dev/null
      else
        xdg-open reviews/health_dashboard.png 2>/dev/null
      fi
      echo '{"systemMessage": "Dashboard regenerated and opened for review."}'
    fi
  fi
}
