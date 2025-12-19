import asyncio
import os
from playwright.async_api import async_playwright
import aiofiles
import aiohttp
BASE_URL = "https://sandesh.com/epaper/ahmedabad?date=2025-12-15"

SAVE_ROOT = "Sandesh"
NEXT_BTN = "span.carousel-control-next-icon"
ARTICLES_PARENT = "div.row.mt-5"
ARTICLE_BLOCK = "div.single-blog img"
abc=[]
dicto={}

async def download_image(url, save_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(save_path, "wb") as f:
                    await f.write(await resp.read())


async def scrape_sandesh():
    os.makedirs(SAVE_ROOT, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)

        # Wait for first page articles
        await page.wait_for_selector(ARTICLES_PARENT)

        current_page = 1
        last_articles_signature = None

        while True:
            print(f"\n[Page {current_page}] Processing")

            # Create page folder
            # page_dir = os.path.join(SAVE_ROOT, f"page_{current_page:02d}")
            # os.makedirs(page_dir, exist_ok=True)

            # Wait for images to fully load
            await page.wait_for_function(
                """() => {
                    const imgs = document.querySelectorAll("div.single-blog img");
                    return imgs.length > 0 && [...imgs].every(i => i.complete);
                }""",
                timeout=10000
            )

            articles = page.locator(ARTICLE_BLOCK)
            count = await articles.count()

            print(f"[Page {current_page}] Articles detected: {count}")

            # Save article images
            for i in range(count):
                img = articles.nth(i)
                src = await img.get_attribute("src")
                abc.append(src)
                dicto[f"page_{current_page}_img_{i+1}.jpg"]=src
                if not src:
                    continue

                img_path = os.path.join(
                SAVE_ROOT,
                f"page_{current_page}_img_{i+1}.jpg"
)
                await download_image(src, img_path)

            # Capture article DOM signature
            current_signature = await page.evaluate(
                """() => {
                    return [...document.querySelectorAll("div.single-blog img")]
                        .map(i => i.src).join("|");
                }"""
            )

            # Stop if page content does not change (LAST PAGE)
            if current_signature == last_articles_signature:
                print("✔ Last page reached (content unchanged)")
                break

            last_articles_signature = current_signature

            # Check NEXT button
            next_btn = page.locator(NEXT_BTN)
            if not await next_btn.is_visible():
                print("✔ Last page reached (no NEXT button)")
                break

            print("[Action] NEXT →")
            await next_btn.click(force=True)
            await asyncio.sleep(1)

            current_page += 1

        await browser.close()
        print("\n✔ Scraping complete")
        print("List:",abc)
        print("-----------------------------------------------------")
        print("Dicto:",dicto)

if __name__ == "__main__":
    asyncio.run(scrape_sandesh())
