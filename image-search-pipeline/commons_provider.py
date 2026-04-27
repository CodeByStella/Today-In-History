"""
Resolve image_search_keywords to HTTPS image URLs using the Wikimedia Commons API.

No API key required. Follows https://wikimediafoundation.org/wiki/Policy:User-Agent
"""

from __future__ import annotations

import time
from typing import Any
from urllib.parse import urlencode

import httpx

COMMONS_API = "https://commons.wikimedia.org/w/api.php"

# Identify this tool to Wikimedia (required); customize contact URL if you fork.
DEFAULT_USER_AGENT = (
    "TodayInHistory-ImagePipeline/1.0 "
    "(Today-In-History hub / image-search-pipeline; +https://github.com/) "
    "python-httpx"
)


def _client(user_agent: str | None = None) -> httpx.Client:
    return httpx.Client(
        headers={"User-Agent": user_agent or DEFAULT_USER_AGENT},
        timeout=httpx.Timeout(30.0),
        follow_redirects=True,
    )


def search_file_titles(client: httpx.Client, query: str, *, limit: int = 8) -> list[str]:
    """Return File: page titles from Commons file search (namespace 6)."""
    params: dict[str, Any] = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query.strip(),
        "srnamespace": 6,
        "srlimit": min(max(limit, 1), 50),
    }
    r = client.get(COMMONS_API, params=params)
    r.raise_for_status()
    data = r.json()
    hits = data.get("query", {}).get("search") or []
    out: list[str] = []
    for h in hits:
        t = h.get("title")
        if isinstance(t, str) and t.startswith("File:"):
            out.append(t)
    return out


def image_urls_for_titles(client: httpx.Client, titles: list[str]) -> list[str]:
    """Fetch direct image URLs for up to 50 File: titles in one request."""
    if not titles:
        return []
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "titles": "|".join(titles),
        "iiprop": "url|mime",
    }
    r = client.get(COMMONS_API, params=params)
    r.raise_for_status()
    data = r.json()
    pages = data.get("query", {}).get("pages") or {}
    urls: list[str] = []
    for _pid, page in pages.items():
        if page.get("missing"):
            continue
        ii = page.get("imageinfo") or []
        if not ii:
            continue
        url = ii[0].get("url")
        mime = ii[0].get("mime") or ""
        if isinstance(url, str) and url.startswith("https://") and mime.startswith("image/"):
            urls.append(url)
    return urls


def head_ok_image(client: httpx.Client, url: str) -> bool:
    """Optional quick check that URL responds with an image/* type."""
    try:
        r = client.head(url, timeout=15.0)
        ct = r.headers.get("content-type", "").split(";")[0].strip().lower()
        return r.is_success and ct.startswith("image/")
    except httpx.HTTPError:
        return False


def resolve_keywords_to_urls(
    client: httpx.Client,
    keywords: list[str],
    *,
    max_urls: int = 3,
    titles_per_keyword: int = 4,
    pause_sec: float = 0.35,
    verify_head: bool = False,
) -> list[str]:
    """
    Run keyword searches until max_urls distinct image URLs are collected.
    """
    collected: list[str] = []
    seen: set[str] = set()

    for kw in keywords:
        if len(collected) >= max_urls:
            break
        if pause_sec > 0:
            time.sleep(pause_sec)
        try:
            titles = search_file_titles(client, kw, limit=titles_per_keyword)
        except httpx.HTTPError:
            continue
        if not titles:
            continue
        # Ask imageinfo in small batches to avoid huge URLs
        batch = titles[: min(6, len(titles))]
        if pause_sec > 0:
            time.sleep(pause_sec)
        try:
            urls = image_urls_for_titles(client, batch)
        except httpx.HTTPError:
            continue
        for u in urls:
            if u in seen:
                continue
            if verify_head and not head_ok_image(client, u):
                continue
            collected.append(u)
            seen.add(u)
            if len(collected) >= max_urls:
                break

    return collected[:max_urls]
