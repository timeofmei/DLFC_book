# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "tqdm",
# ]
# ///

import asyncio
import httpx
from pathlib import Path
from tqdm.asyncio import tqdm

BASE_URL = "https://svg.issuu.com/250712151426-cf4048364da52d8d0cbf6421a2e07a54/page_{i}.svg"
OUTPUT_DIR = Path(__file__).parent / "svg"
TOTAL_PAGES = 666
CONCURRENCY_LIMIT = 10

async def download_file(client, page_num, semaphore):
    url = BASE_URL.format(i=page_num)
    file_path = OUTPUT_DIR / f"page_{page_num}.svg"
    
    if file_path.exists():
        # Optional: Check file size to ensure it wasn't a partial download
        return

    async with semaphore:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            file_path.write_bytes(response.content)
        except Exception as e:
            print(f"Failed to download page {page_num}: {e}")

async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    
    print(f"Downloading {TOTAL_PAGES} SVGs to {OUTPUT_DIR}...")
    
    async with httpx.AsyncClient() as client:
        tasks = [download_file(client, i, semaphore) for i in range(1, TOTAL_PAGES + 1)]
        await tqdm.gather(*tasks, desc="Progress")

if __name__ == "__main__":
    asyncio.run(main())
