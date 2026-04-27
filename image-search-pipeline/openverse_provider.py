"""
Fallback image search via Openverse (CC-licensed index; anonymous rate limits apply).

https://api.openverse.engineering — see response headers for X-RateLimit-*.
"""

from __future__ import annotations

import re
import time
from typing import Any, Sequence

import httpx

OPENVERSE_IMAGES = "https://api.openverse.engineering/v1/images/"


def search_openverse_image_urls(
    client: httpx.Client,
    query: str,
    *,
    page_size: int = 8,
) -> list[str]:
    """Return direct image URLs from Openverse search results."""
    r = client.get(
        OPENVERSE_IMAGES,
        params={"q": query.strip(), "page_size": min(max(page_size, 1), 20)},
    )
    r.raise_for_status()
    data: dict[str, Any] = r.json()
    out: list[str] = []
    for item in data.get("results") or []:
        u = item.get("url")
        if isinstance(u, str) and u.startswith("https://"):
            out.append(u)
    return out


def _openverse_query_variants(kw: str) -> list[str]:
    """Openverse works best on short Latin queries; derive a few variants from a long JP/EN mix."""
    base = kw.strip()
    out: list[str] = []
    if base:
        out.append(base)
    if len(base) > 48:
        out.append(base[:48].strip())
    ascii_tokens = re.findall(r"[A-Za-z][A-Za-z0-9\-]{2,}", base)
    if ascii_tokens:
        out.append(" ".join(ascii_tokens)[:80])
    digits = re.findall(r"\d{4}", base)
    if ascii_tokens and digits:
        out.append(f"{ascii_tokens[0]} {digits[0]}"[:80])
    # de-dupe, keep order
    seen_q: set[str] = set()
    uniq: list[str] = []
    for q in out:
        if q and q not in seen_q:
            seen_q.add(q)
            uniq.append(q)
    return uniq


def top_up_urls(
    client: httpx.Client,
    keywords: list[str],
    *,
    need: int,
    seen: set[str],
    pause_sec: float,
    verify_head: bool,
    extra_queries: Sequence[str] = (),
) -> list[str]:
    """Collect up to `need` new URLs using Openverse."""
    from commons_provider import head_ok_image

    found: list[str] = []
    if need <= 0:
        return found

    # Prefer keywords that contain Latin letters/digits (Openverse matches poorly on long JP-only strings).
    kw_sorted = sorted(
        keywords,
        key=lambda s: sum(1 for c in s if c.isascii() and (c.isalpha() or c.isdigit())),
        reverse=True,
    )
    ordered_queries: list[str] = []
    for kw in kw_sorted:
        ordered_queries.extend(_openverse_query_variants(kw))
    for eq in extra_queries:
        s = (eq or "").strip()
        if len(s) >= 4:
            ordered_queries.extend(_openverse_query_variants(s))

    seen_q: set[str] = set()
    deduped_queries: list[str] = []
    for q in ordered_queries:
        if q not in seen_q:
            seen_q.add(q)
            deduped_queries.append(q)

    for q in deduped_queries:
        if len(found) >= need:
            break
        if pause_sec > 0:
            time.sleep(pause_sec)
        try:
            candidates = search_openverse_image_urls(client, q, page_size=12)
        except httpx.HTTPError:
            continue
        for u in candidates:
            if u in seen:
                continue
            if verify_head and not head_ok_image(client, u):
                continue
            found.append(u)
            seen.add(u)
            if len(found) >= need:
                break
    return found
