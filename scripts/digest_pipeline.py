"""
Knowledge-hub Digest Pipeline
Combines Gmail newsletters + X scraper results into a unified digest.
Uses inline CSS (no CDN dependency).
"""

import hashlib
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

TST = timezone(timedelta(hours=8))

ROUTE_CONFIG = {
    "pharma-decipher": {"skill": "/pda-doc", "domain": "Pharma", "color": "#dc2626"},
    "hbr-review": {"skill": "/hbr-single", "domain": "Leadership", "color": "#4f46e5"},
    "ai-articles": {"skill": "/ai-doc", "domain": "AI", "color": "#0891b2"},
}

PURPLE = "#482A77"
PURPLE_LIGHT = "#6B4A9E"


def load_x_results(path: str) -> list[dict]:
    """Load X scraper JSON output, deduplicate by content hash."""
    p = Path(path)
    if not p.exists():
        print(f"Warning: {path} not found, skipping X results")
        return []

    data = json.loads(p.read_text())
    articles = []
    seen = set()

    for account in data.get("accounts", []):
        if account["status"] != "found":
            continue
        for tweet in account["tweets"]:
            if not tweet.get("within_24h"):
                continue
            content_hash = hashlib.md5(tweet["text"].encode()).hexdigest()
            if content_hash in seen:
                continue
            seen.add(content_hash)
            articles.append({
                "source": f"X/@{account['username']}",
                "source_type": "x",
                "title": tweet["text"][:80] + ("..." if len(tweet["text"]) > 80 else ""),
                "content": tweet["text"],
                "timestamp_tst": tweet.get("timestamp_tst", ""),
                "url": tweet.get("url", f"https://x.com/{account['username']}"),
                "route": account["route"],
                "domain": account["domain"],
                "label": account["label"],
            })
    return articles


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def generate_combined_html(gmail_articles, x_articles, output_path):
    now = datetime.now(TST)
    all_articles = gmail_articles + x_articles

    by_route = {}
    for i, a in enumerate(all_articles):
        route = a.get("route", "ai-articles")
        by_route.setdefault(route, []).append((i, a))

    # Build cards
    cards = ""
    for route, items in by_route.items():
        cfg = ROUTE_CONFIG.get(route, {"skill": "N/A", "domain": route, "color": "#666"})
        cards += f'<div style="margin-bottom:32px;">'
        cards += f'<h2 style="font-size:16px;font-weight:700;color:#1f2937;margin-bottom:12px;">'
        cards += f'<span style="background:{PURPLE};color:#fff;padding:2px 8px;border-radius:4px;font-size:11px;margin-right:8px;">{route}</span>'
        cards += f'{cfg["domain"]} → <code style="background:#f3f4f6;padding:2px 6px;border-radius:4px;font-size:13px;">{cfg["skill"]}</code></h2>'

        for idx, article in items:
            content = _esc(article.get("content", "")).replace("\n", "<br>")
            is_long = len(article.get("content", "")) > 200
            source_type = article.get("source_type", "email")
            badge_bg = "#ecfeff" if source_type == "x" else "#f0fdf4"
            badge_color = "#0e7490" if source_type == "x" else "#15803d"
            badge_text = "X" if source_type == "x" else "Email"

            cards += f'''
<div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;padding:16px;margin-bottom:10px;">
  <div style="display:flex;gap:12px;align-items:flex-start;">
    <input type="checkbox" class="cb" data-idx="{idx}" data-route="{route}" style="margin-top:4px;width:16px;height:16px;cursor:pointer;">
    <div style="flex:1;min-width:0;">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <span style="background:{badge_bg};color:{badge_color};border:1px solid {badge_color}30;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600;">{badge_text}</span>
        <span style="font-size:12px;color:#6b7280;font-weight:500;">{_esc(article.get("source", ""))}</span>
        <span style="font-size:12px;color:#9ca3af;">|</span>
        <span style="font-size:12px;color:#6b7280;">{article.get("timestamp_tst", "")}</span>
      </div>
      <div id="c{idx}" style="font-size:14px;color:#1f2937;line-height:1.7;{"max-height:100px;overflow:hidden;" if is_long else ""}">
        {content}
      </div>
      {"<button onclick='tog(" + str(idx) + ")' id='b" + str(idx) + "' style=" + '"font-size:12px;color:' + PURPLE + ';background:none;border:none;cursor:pointer;padding:4px 0;font-weight:600;"' + ">Show more ↓</button>" if is_long else ""}
      <div style="display:flex;align-items:center;justify-content:space-between;margin-top:10px;padding-top:8px;border-top:1px solid #f3f4f6;">
        <span style="font-size:11px;color:#9ca3af;">{_esc(article.get("label", ""))}</span>
        {"<a href='" + article["url"] + "' target='_blank' style='font-size:12px;background:" + PURPLE + ";color:#fff;padding:4px 12px;border-radius:4px;text-decoration:none;'>Read →</a>" if article.get("url") else ""}
      </div>
    </div>
  </div>
</div>'''

        cards += '</div>'

    # X status
    x_status = ""
    x_json = Path("scripts/x_latest.json")
    if x_json.exists():
        data = json.loads(x_json.read_text())
        rows = ""
        for acc in data.get("accounts", []):
            icon = {"found": "✔", "no_recent": "⚠", "empty": "✗", "error": "✗"}.get(acc["status"], "?")
            clr = {"found": "#16a34a", "no_recent": "#ca8a04", "empty": "#9ca3af", "error": "#dc2626"}.get(acc["status"], "#666")
            detail = ""
            if acc["status"] == "found":
                detail = f"({len(acc['tweets'])} tweets)"
            elif acc["status"] == "no_recent":
                detail = f"— 0 in 24hr (last: {acc.get('last_tweet_time', 'unknown')})"
            rows += f'<div><span style="color:{clr};font-weight:700;">{icon}</span> @{acc["username"]} {detail}</div>'
        x_status = f'<div style="background:#f3f4f6;border-radius:8px;padding:12px;margin-bottom:16px;"><div style="font-size:13px;font-weight:600;color:#374151;margin-bottom:8px;">X/Twitter Source Status</div><div style="font-size:12px;line-height:1.8;">{rows}</div></div>'

    articles_json = json.dumps(all_articles, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Daily Digest — {now.strftime('%Y-%m-%d')}</title>
</head>
<body style="margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#fff;min-height:100vh;padding-bottom:80px;">

<div style="background:linear-gradient(135deg,{PURPLE},{PURPLE_LIGHT});color:#fff;padding:16px 20px;">
  <h1 style="margin:0;font-size:20px;">Daily Digest — {now.strftime('%Y-%m-%d')}</h1>
  <p style="margin:4px 0 0;font-size:12px;opacity:0.8;">Gmail Newsletters + X/Twitter | {now.strftime('%H:%M')} TST</p>
  <p style="margin:2px 0 0;font-size:12px;opacity:0.8;">✔ 24hr filter active | Since {(now - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M')} TST</p>
</div>

<div style="max-width:720px;margin:0 auto;padding:16px;">

  <div style="display:flex;gap:12px;margin-bottom:16px;font-size:13px;">
    <span style="background:#f3f4f6;padding:4px 12px;border-radius:4px;">Total: <strong>{len(all_articles)}</strong></span>
    <span style="background:#f0fdf4;padding:4px 12px;border-radius:4px;color:#15803d;">Email: <strong>{len(gmail_articles)}</strong></span>
    <span style="background:#ecfeff;padding:4px 12px;border-radius:4px;color:#0e7490;">X: <strong>{len(x_articles)}</strong></span>
  </div>

  {x_status}

  <div style="margin-bottom:16px;">
    <label style="display:flex;align-items:center;gap:8px;cursor:pointer;font-size:13px;color:#4b5563;">
      <input type="checkbox" id="sa" style="width:16px;height:16px;cursor:pointer;"> Select All
    </label>
  </div>

  {cards}
</div>

<div id="bar" style="display:none;position:fixed;bottom:0;left:0;right:0;background:#fff;box-shadow:0 -2px 8px rgba(0,0,0,0.1);border-top:1px solid #e5e7eb;padding:12px 20px;display:none;align-items:center;justify-content:space-between;z-index:50;">
  <span id="cnt" style="font-size:14px;color:#374151;">0 selected</span>
  <button onclick="exp()" style="background:{PURPLE};color:#fff;padding:8px 16px;border-radius:6px;border:none;font-size:13px;cursor:pointer;">Export & Generate Docs →</button>
</div>

<div id="modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:100;justify-content:center;align-items:center;">
  <div style="background:#fff;border-radius:12px;padding:24px;max-width:640px;width:calc(100% - 32px);max-height:80vh;overflow-y:auto;">
    <h2 style="margin:0 0 16px;font-size:18px;">Export — Ready for Doc Generation</h2>
    <pre id="out" style="background:#f9fafb;padding:16px;border-radius:8px;font-size:12px;white-space:pre-wrap;border:1px solid #e5e7eb;line-height:1.6;"></pre>
    <div style="display:flex;gap:8px;margin-top:16px;">
      <button onclick="cpx()" id="cpb" style="background:{PURPLE};color:#fff;padding:8px 16px;border-radius:6px;border:none;cursor:pointer;font-size:13px;">Copy to Clipboard</button>
      <button onclick="document.getElementById('modal').style.display='none'" style="background:#e5e7eb;color:#374151;padding:8px 16px;border-radius:6px;border:none;cursor:pointer;font-size:13px;">Close</button>
    </div>
  </div>
</div>

<script>
const A={articles_json};
document.getElementById('sa').onchange=function(){{document.querySelectorAll('.cb').forEach(c=>c.checked=this.checked);uc();}};
document.querySelectorAll('.cb').forEach(c=>c.onchange=uc);
function uc(){{const n=document.querySelectorAll('.cb:checked').length;const b=document.getElementById('bar');b.style.display=n>0?'flex':'none';document.getElementById('cnt').textContent=n+' selected';}}
function tog(i){{const c=document.getElementById('c'+i),b=document.getElementById('b'+i);if(c.style.maxHeight==='100px'){{c.style.maxHeight='none';c.style.overflow='visible';b.textContent='Show less ↑';}}else{{c.style.maxHeight='100px';c.style.overflow='hidden';b.textContent='Show more ↓';}}}}
function exp(){{const cbs=document.querySelectorAll('.cb:checked');const R={{}};cbs.forEach(c=>{{const i=+c.dataset.idx,r=c.dataset.route;(R[r]=R[r]||[]).push(A[i]);}});let t='Daily Digest Export — {now.strftime("%Y-%m-%d")}\\nSelected: '+cbs.length+' articles\\n\\n===============================================\\n';for(const[r,items]of Object.entries(R)){{t+='\\n>> '+r.toUpperCase()+'\\n-----------------------------------------------\\n\\n';items.forEach(a=>{{t+='['+a.source+'] '+a.timestamp_tst+'\\n'+a.content+'\\n';if(a.url)t+='Link: '+a.url+'\\n';t+='\\n---\\n\\n';}});}}t+='===============================================\\n\\nRouting Summary:\\n';for(const[r,items]of Object.entries(R))t+='  '+r+': '+items.length+' articles\\n';document.getElementById('out').textContent=t;document.getElementById('modal').style.display='flex';}}
function cpx(){{navigator.clipboard.writeText(document.getElementById('out').textContent);const b=document.getElementById('cpb');b.textContent='Copied!';setTimeout(()=>b.textContent='Copy to Clipboard',2000);}}
</script>
</body>
</html>"""

    Path(output_path).write_text(html)
    print(f"Digest HTML saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    x_articles = load_x_results("scripts/x_latest.json")
    print(f"Loaded {len(x_articles)} X articles (deduplicated)")
    gmail_articles = []
    output = sys.argv[1] if len(sys.argv) > 1 else "scripts/digest_combined.html"
    generate_combined_html(gmail_articles, x_articles, output)
