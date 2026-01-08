import aiohttp
import asyncio
from aiohttp import ClientTimeout

# RẤT NHIỀU nguồn proxy HTTP
PROXY_SOURCES = [
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxyscan.io/download?type=http",
    "https://www.proxyscan.io/download?type=https",

    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/https.txt",

    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt",

    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/https.txt",

    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt"
]

OUTPUT_FILE = "proxy.txt"


async def fetch_proxies(url):
    try:
        async with aiohttp.ClientSession(
            timeout=ClientTimeout(total=15)
        ) as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    print(f"✔ Lấy proxy từ: {url}")
                    return await resp.text()
    except Exception as e:
        print(f"✘ Lỗi {url}: {e}")
    return ""


async def main():
    print("🚀 Đang lấy proxy từ các nguồn...")

    tasks = [fetch_proxies(url) for url in PROXY_SOURCES]
    results = await asyncio.gather(*tasks)

    proxies = set()  # dùng set để tự động loại trùng

    for text in results:
        for line in text.splitlines():
            line = line.strip()
            if line and ":" in line:
                proxies.add(line)

    print(f"✅ Tổng proxy thu được (không trùng): {len(proxies)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(proxies))

    print(f"💾 Đã lưu vào {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
