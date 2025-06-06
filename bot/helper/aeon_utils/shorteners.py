from asyncio import sleep
from random import choice
from urllib.parse import quote

from aiohttp import ClientSession
from pyshorteners import Shortener

from bot import shorteners_list


async def short(long_url):
    """
    Shortens a given long URL using a randomly chosen shortener from a predefined list,
    with a fallback to TinyURL if custom shorteners fail or are not configured.

    Args:
        long_url: The long URL to be shortened.

    Returns:
        A shortened URL string, or the original long_url if all shortening attempts fail.
    """
    if not shorteners_list:
        return long_url

    async with ClientSession() as session:
        for _attempt in range(4):
            shortener_info = choice(shorteners_list)
            try:
                async with session.get(
                    f"https://{shortener_info['domain']}/api?api={shortener_info['api_key']}&url={quote(long_url)}",
                ) as response:
                    result = await response.json()
                    short_url = result.get("shortenedUrl", long_url)
                    if short_url != long_url:
                        long_url = short_url
                        break
            except Exception:
                continue

        s = Shortener()
        for _attempt in range(4):
            try:
                return s.tinyurl.short(long_url)
            except Exception:
                await sleep(1)

        return long_url
