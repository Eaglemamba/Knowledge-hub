#!/usr/bin/env bash
# stop-notify.sh
# Plays a notification sound on session end. Cross-platform.

if [[ "$OSTYPE" == "darwin"* ]]; then
  afplay /System/Library/Sounds/Blow.aiff
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]] || grep -qi microsoft /proc/version 2>/dev/null; then
  powershell.exe -c '[System.Media.SystemSounds]::Exclamation.Play()' 2>/dev/null || rundll32.exe user32.dll,MessageBeep 2>/dev/null
else
  paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null || aplay /usr/share/sounds/sound-icons/trumpet-12.wav 2>/dev/null || true
fi
