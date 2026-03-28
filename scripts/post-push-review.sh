#!/usr/bin/env bash
# post-push-review.sh
# Generates a temporary HTML review page for recently pushed HTML, MD, and image files.
# Designed to be called from a Claude Code PostToolUse hook after git push.

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
REPO_NAME=$(basename "$REPO_ROOT")
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Get changed files from the last pushed commit
CHANGED=$(git diff HEAD~1 --name-only --diff-filter=ACMR 2>/dev/null || true)
[ -z "$CHANGED" ] && exit 0

# Filter by type
HTML_FILES=$(echo "$CHANGED" | grep -iE '\.html$' || true)
MD_FILES=$(echo "$CHANGED" | grep -iE '\.md$' || true)
IMG_FILES=$(echo "$CHANGED" | grep -iE '\.(png|jpg|jpeg|gif|svg|webp)$' || true)

# Exit if nothing relevant
if [ -z "$HTML_FILES" ] && [ -z "$MD_FILES" ] && [ -z "$IMG_FILES" ]; then
  exit 0
fi

# Count files
html_count=$(echo "$HTML_FILES" | grep -c '.' 2>/dev/null || echo 0)
md_count=$(echo "$MD_FILES" | grep -c '.' 2>/dev/null || echo 0)
img_count=$(echo "$IMG_FILES" | grep -c '.' 2>/dev/null || echo 0)
total=$((html_count + md_count + img_count))

# Create temp review file
REVIEW_FILE=$(mktemp /tmp/push-review-XXXXXX.html)

cat > "$REVIEW_FILE" << 'HEADER'
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Push Review</title>
<style>
  :root { --bg: #0d1117; --card: #161b22; --border: #30363d; --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --orange: #d29922; --purple: #bc8cff; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); padding: 2rem; line-height: 1.6; }
  .header { text-align: center; margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border); }
  .header h1 { font-size: 1.5rem; margin-bottom: 0.5rem; }
  .meta { color: var(--muted); font-size: 0.85rem; }
  .meta span { margin: 0 0.5rem; }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
  .badge-html { background: rgba(88,166,255,0.15); color: var(--accent); }
  .badge-md { background: rgba(63,185,80,0.15); color: var(--green); }
  .badge-img { background: rgba(188,140,255,0.15); color: var(--purple); }
  .section { margin-bottom: 2rem; }
  .section h2 { font-size: 1.1rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }
  .file-card { background: var(--card); border: 1px solid var(--border); border-radius: 8px; margin-bottom: 1rem; overflow: hidden; }
  .file-card-header { padding: 0.75rem 1rem; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
  .file-card-header code { font-size: 0.85rem; color: var(--accent); }
  .file-card-body { padding: 1rem; }
  .file-card-body pre { white-space: pre-wrap; word-wrap: break-word; font-size: 0.8rem; color: var(--muted); max-height: 400px; overflow-y: auto; }
  .file-card-body img { max-width: 100%; max-height: 500px; border-radius: 4px; }
  .open-btn { display: inline-block; padding: 4px 12px; background: rgba(88,166,255,0.15); color: var(--accent); border: 1px solid rgba(88,166,255,0.3); border-radius: 6px; text-decoration: none; font-size: 0.8rem; cursor: pointer; }
  .open-btn:hover { background: rgba(88,166,255,0.25); }
  .iframe-wrap { width: 100%; height: 600px; border: 1px solid var(--border); border-radius: 4px; overflow: hidden; }
  .iframe-wrap iframe { width: 100%; height: 100%; border: none; }
  .summary { display: flex; gap: 1rem; justify-content: center; margin: 1rem 0; flex-wrap: wrap; }
  .summary-item { background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem 1.5rem; text-align: center; }
  .summary-item .num { font-size: 1.5rem; font-weight: 700; }
  .summary-item .label { font-size: 0.75rem; color: var(--muted); }
</style>
</head>
<body>
HEADER

# Write header with repo info
cat >> "$REVIEW_FILE" << EOF
<div class="header">
  <h1>Push Review</h1>
  <div class="meta">
    <span><strong>${REPO_NAME}</strong></span>
    <span>/</span>
    <span>${BRANCH}</span>
    <span>|</span>
    <span>${TIMESTAMP}</span>
  </div>
  <div class="summary">
    <div class="summary-item"><div class="num" style="color:var(--accent)">${html_count}</div><div class="label">HTML</div></div>
    <div class="summary-item"><div class="num" style="color:var(--green)">${md_count}</div><div class="label">Markdown</div></div>
    <div class="summary-item"><div class="num" style="color:var(--purple)">${img_count}</div><div class="label">Images</div></div>
  </div>
</div>
EOF

# --- HTML Files ---
if [ -n "$HTML_FILES" ]; then
  cat >> "$REVIEW_FILE" << 'EOF'
<div class="section">
  <h2><span class="badge badge-html">HTML</span> Page Updates</h2>
EOF
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    full_path="${REPO_ROOT}/${f}"
    cat >> "$REVIEW_FILE" << EOF
  <div class="file-card">
    <div class="file-card-header">
      <code>${f}</code>
      <a class="open-btn" href="file://${full_path}" target="_blank">Open File</a>
    </div>
    <div class="file-card-body">
      <div class="iframe-wrap">
        <iframe src="file://${full_path}" sandbox="allow-same-origin"></iframe>
      </div>
    </div>
  </div>
EOF
  done <<< "$HTML_FILES"
  echo "</div>" >> "$REVIEW_FILE"
fi

# --- Markdown Files ---
if [ -n "$MD_FILES" ]; then
  cat >> "$REVIEW_FILE" << 'EOF'
<div class="section">
  <h2><span class="badge badge-md">MD</span> Markdown Updates</h2>
EOF
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    full_path="${REPO_ROOT}/${f}"
    # Read file content safely and escape HTML
    if [ -f "$full_path" ]; then
      content=$(sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g' "$full_path" | head -100)
    else
      content="(file not found)"
    fi
    cat >> "$REVIEW_FILE" << EOF
  <div class="file-card">
    <div class="file-card-header">
      <code>${f}</code>
      <a class="open-btn" href="file://${full_path}" target="_blank">Open File</a>
    </div>
    <div class="file-card-body">
      <pre>${content}</pre>
    </div>
  </div>
EOF
  done <<< "$MD_FILES"
  echo "</div>" >> "$REVIEW_FILE"
fi

# --- Image Files ---
if [ -n "$IMG_FILES" ]; then
  cat >> "$REVIEW_FILE" << 'EOF'
<div class="section">
  <h2><span class="badge badge-img">IMG</span> Image Updates</h2>
EOF
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    full_path="${REPO_ROOT}/${f}"
    cat >> "$REVIEW_FILE" << EOF
  <div class="file-card">
    <div class="file-card-header">
      <code>${f}</code>
      <a class="open-btn" href="file://${full_path}" target="_blank">Open File</a>
    </div>
    <div class="file-card-body" style="text-align:center; background:#1c2128; padding:1.5rem;">
      <img src="file://${full_path}" alt="${f}">
    </div>
  </div>
EOF
  done <<< "$IMG_FILES"
  echo "</div>" >> "$REVIEW_FILE"
fi

# Close HTML
cat >> "$REVIEW_FILE" << 'FOOTER'
<div style="text-align:center; color:var(--muted); font-size:0.75rem; margin-top:2rem; padding-top:1rem; border-top:1px solid var(--border);">
  Generated by Knowledge-hub Post-Push Review Hook
</div>
</body>
</html>
FOOTER

# Open the review page
open "$REVIEW_FILE" 2>/dev/null || xdg-open "$REVIEW_FILE" 2>/dev/null || true

# Report back to Claude Code
echo "{\"systemMessage\": \"Push review opened — ${total} file(s) changed: ${html_count} HTML, ${md_count} MD, ${img_count} images.\"}"
