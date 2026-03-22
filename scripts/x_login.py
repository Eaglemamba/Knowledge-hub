"""
Open a browser for manual X/Twitter login.
Session is saved to ~/knowledge-hub/.pw-profile for future scraping.
Uses anti-detection args to avoid X blocking.

Usage: python scripts/x_login.py
"""

import asyncio
import os

from playwright.async_api import async_playwright

STEALTH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--disable-infobars",
    "--no-first-run",
    "--no-default-browser-check",
]


async def login():
    async with async_playwright() as p:
        profile_path = os.path.expanduser("~/knowledge-hub/.pw-profile")

        # Clear old profile if exists
        import shutil
        if os.path.exists(profile_path):
            shutil.rmtree(profile_path)

        context = await p.chromium.launch_persistent_context(
            profile_path,
            headless=False,
            channel="chrome",
            viewport={"width": 1280, "height": 800},
            args=STEALTH_ARGS,
            ignore_default_args=["--enable-automation"],
        )

        # Remove webdriver flag via JS
        for page in context.pages:
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            """)

        page = context.pages[0] if context.pages else await context.new_page()
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)
        await page.goto("https://x.com/login")

        print("Browser opened — please log in to X.")
        print("The automation banner should be gone now.")
        print("Waiting for login (checking every 3 seconds)...")

        # Poll for login success (max 180 seconds)
        for i in range(60):
            await asyncio.sleep(3)
            url = page.url
            if "login" not in url and "flow" not in url:
                print(f"\nLOGIN SUCCESS — URL: {url}")
                print("Session saved to: ~/knowledge-hub/.pw-profile")
                await asyncio.sleep(3)
                await context.close()
                return True

        print("\nTimeout — login not detected after 180 seconds.")
        await context.close()
        return False


if __name__ == "__main__":
    result = asyncio.run(login())
    exit(0 if result else 1)
