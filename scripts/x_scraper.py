"""
X/Twitter Scraper for Knowledge-hub Daily Digest
Uses playwright with logged-in session to scrape latest tweets.
Filters by 24-hour window (TST timezone).

Prerequisites:
  Run x_login.py first to save session to ~/.pw-profile
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from playwright.async_api import async_playwright

TST = timezone(timedelta(hours=8))

STEALTH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--disable-infobars",
]

ACCOUNTS = [
    {"username": "karpathy", "domain": "ai", "label": "Andrej Karpathy"},
    {"username": "trq212", "domain": "ai", "label": "trq212"},
    {"username": "bcherny", "domain": "ai", "label": "Boris Cherny"},
    {"username": "emollick", "domain": "leadership", "label": "Ethan Mollick"},
    {"username": "A_May_MD", "domain": "pharma", "label": "A_May_MD"},
    {"username": "HiTw93", "domain": "ai", "label": "Tw93"},
]

# Domain to agent route mapping (matches daily-news-digest)
DOMAIN_ROUTE = {
    "ai": "ai-articles",
    "pharma": "pharma-decipher",
    "leadership": "hbr-review",
}


async def scrape_account(page, account: dict, cutoff: datetime) -> dict:
    """Scrape tweets from a single X account, filter by 24hr window."""
    username = account["username"]
    result = {
        "username": username,
        "label": account["label"],
        "domain": account["domain"],
        "route": DOMAIN_ROUTE.get(account["domain"], "ai-articles"),
        "status": "error",
        "tweets": [],
    }

    try:
        await page.goto(f"https://x.com/{username}", timeout=15000)
        await page.wait_for_timeout(5000)

        # Scroll down to load more tweets
        await page.evaluate("window.scrollBy(0, 800)")
        await page.wait_for_timeout(2000)

        # Parse at article level to detect pinned tweets
        articles = await page.query_selector_all("article")

        all_tweets = []
        within_24h = []

        for article in articles[:12]:
            # Skip pinned tweets
            article_html = await article.inner_html()
            if "Pinned" in article_html:
                continue

            text_el = await article.query_selector('[data-testid="tweetText"]')
            time_el = await article.query_selector("time")
            if not text_el or not time_el:
                continue

            text = await text_el.inner_text()
            ts_str = await time_el.get_attribute("datetime")

            tweet_data = {
                "text": text.strip(),
                "timestamp_utc": ts_str,
                "timestamp_tst": None,
                "within_24h": False,
                "url": f"https://x.com/{username}",
            }

            if ts_str:
                try:
                    dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    tweet_data["timestamp_tst"] = dt.astimezone(TST).strftime(
                        "%Y-%m-%d %H:%M TST"
                    )
                    if dt >= cutoff:
                        tweet_data["within_24h"] = True
                        within_24h.append(tweet_data)
                except ValueError:
                    pass

            all_tweets.append(tweet_data)

        if within_24h:
            result["status"] = "found"
            result["tweets"] = within_24h
        elif all_tweets:
            result["status"] = "no_recent"
            result["tweets"] = all_tweets[:1]
            result["last_tweet_time"] = all_tweets[0].get("timestamp_tst", "unknown")
        else:
            result["status"] = "empty"

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


async def scrape_all(output_path: str | None = None) -> list[dict]:
    """Scrape all tracked X accounts using logged-in session."""
    now_tst = datetime.now(TST)
    cutoff = now_tst - timedelta(hours=24)
    cutoff_utc = cutoff.astimezone(timezone.utc)

    profile_path = os.path.expanduser("~/knowledge-hub/.pw-profile")
    if not os.path.exists(profile_path):
        print("ERROR: No session found. Run x_login.py first.")
        return []

    print(f"Current time: {now_tst.strftime('%Y-%m-%d %H:%M TST')}")
    print(f"24hr cutoff:  {cutoff.strftime('%Y-%m-%d %H:%M TST')}")
    print(f"Scraping {len(ACCOUNTS)} X accounts...\n")

    results = []

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            profile_path,
            headless=True,
            channel="chrome",
            args=STEALTH_ARGS,
            ignore_default_args=["--enable-automation"],
        )

        page = context.pages[0] if context.pages else await context.new_page()
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)

        for account in ACCOUNTS:
            print(f"  Scraping @{account['username']}...", end=" ", flush=True)
            result = await scrape_account(page, account, cutoff_utc)

            status_icon = {
                "found": "✔",
                "no_recent": "⚠",
                "empty": "✗",
                "error": "✗",
            }
            icon = status_icon.get(result["status"], "?")
            tweet_count = len([t for t in result["tweets"] if t.get("within_24h")])
            print(f"{icon} ({tweet_count} tweets in 24hr)")

            results.append(result)

        await context.close()

    # Summary
    print("\n--- Source Status ---")
    for r in results:
        icon = {"found": "✔", "no_recent": "⚠", "empty": "✗", "error": "✗"}.get(
            r["status"], "?"
        )
        if r["status"] == "found":
            count = len(r["tweets"])
            print(f"  {icon} @{r['username']} ({count} tweets)")
        elif r["status"] == "no_recent":
            print(
                f"  {icon} @{r['username']} — tweets found, 0 in 24hr (last: {r.get('last_tweet_time', 'unknown')})"
            )
        elif r["status"] == "error":
            print(f"  {icon} @{r['username']} — error: {r.get('error', 'unknown')}")
        else:
            print(f"  {icon} @{r['username']} — no tweets found")

    # Output JSON
    output = {
        "scrape_time_tst": now_tst.isoformat(),
        "cutoff_tst": cutoff.isoformat(),
        "accounts": results,
    }

    if output_path:
        Path(output_path).write_text(json.dumps(output, ensure_ascii=False, indent=2))
        print(f"\nResults saved to: {output_path}")

    return results


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(scrape_all(output))
