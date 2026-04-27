#!/usr/bin/env python3
"""
Image search pipeline — validate events JSON; optionally resolve keywords to image URLs.

Usage:
  python run.py -i path/to/events.json
  python run.py -i path/to/events.json --dry-run
  python run.py -i path/to/events.json --search -o enriched.json
  python run.py -i path/to/events.json --search   # writes enriched JSON to stdout

Image resolution (real HTTP search): **Wikimedia Commons** first, then **Openverse** to fill remaining slots. Install deps:
  pip install -r requirements.txt
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_TOP = ("date", "category", "title", "description", "image_search_keywords")


def validate_record(obj: Any, index: int) -> list[str]:
    errors: list[str] = []
    if not isinstance(obj, dict):
        return [f"[{index}] item is not an object"]
    for key in REQUIRED_TOP:
        if key not in obj:
            errors.append(f"[{index}] missing '{key}'")
    kws = obj.get("image_search_keywords")
    if kws is not None:
        if not isinstance(kws, list):
            errors.append(f"[{index}] image_search_keywords must be an array")
        else:
            if len(kws) < 3:
                errors.append(f"[{index}] image_search_keywords must have at least 3 strings")
            for j, q in enumerate(kws):
                if not isinstance(q, str) or len(q.strip()) < 4:
                    errors.append(f"[{index}] image_search_keywords[{j}] invalid or too short")
                if "http://" in q or "https://" in q.lower():
                    errors.append(f"[{index}] image_search_keywords[{j}] must not contain URLs")
    return errors


def run_web_image_search(
    data: list[dict[str, Any]],
    *,
    max_images: int,
    pause: float,
    verify_head: bool,
    openverse: bool,
) -> None:
    try:
        from commons_provider import _client, resolve_keywords_to_urls
        from openverse_provider import top_up_urls
    except ImportError as e:
        print("Missing dependency. Run: pip install -r requirements.txt", file=sys.stderr)
        print(str(e), file=sys.stderr)
        raise SystemExit(3) from e

    with _client() as client:
        for i, item in enumerate(data):
            kws = [k for k in item.get("image_search_keywords", []) if isinstance(k, str)]
            kws.sort(
                key=lambda s: sum(1 for c in s if c.isascii() and (c.isalpha() or c.isdigit())),
                reverse=True,
            )
            print(f"[{i + 1}/{len(data)}] Image search: {item.get('title', '')[:60]}…", file=sys.stderr)
            urls = resolve_keywords_to_urls(
                client,
                kws,
                max_urls=max_images,
                pause_sec=pause,
                verify_head=verify_head,
            )
            if openverse and len(urls) < max_images:
                need = max_images - len(urls)
                seen = set(urls)
                extra = top_up_urls(
                    client,
                    kws,
                    need=need,
                    seen=seen,
                    pause_sec=pause,
                    verify_head=verify_head,
                    extra_queries=(item.get("title") or "", item.get("subtitle") or ""),
                )
                urls = urls + extra
            item["images"] = urls[:max_images]
            print(f"         → {len(item['images'])} image URL(s)", file=sys.stderr)


def main() -> int:
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    parser = argparse.ArgumentParser(
        description="Validate events JSON; optionally search Wikimedia Commons and fill images."
    )
    parser.add_argument("-i", "--input", type=Path, required=True, help="JSON file: array of event objects")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print one JSON line per keyword job (event index, date, title, keyword)",
    )
    parser.add_argument(
        "--search",
        action="store_true",
        help="Search the web for images from image_search_keywords (Commons + Openverse) and set images[]",
    )
    parser.add_argument(
        "--no-openverse",
        action="store_true",
        help="With --search: use only Wikimedia Commons (no Openverse fallback)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Write enriched JSON here (use with --search). If omitted with --search, print JSON to stdout",
    )
    parser.add_argument("--max-images", type=int, default=3, help="Max image URLs per event (default: 3)")
    parser.add_argument(
        "--pause",
        type=float,
        default=0.35,
        help="Seconds to sleep between Commons API calls (be polite to WM servers; default 0.35)",
    )
    parser.add_argument(
        "--verify-head",
        action="store_true",
        help="HTTP HEAD each image URL and require image/* (slower; may reject some valid CDN URLs)",
    )
    args = parser.parse_args()

    raw = args.input.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        return 2

    if not isinstance(data, list):
        print("Top-level JSON must be an array of events.", file=sys.stderr)
        return 2

    all_errors: list[str] = []
    for i, item in enumerate(data):
        all_errors.extend(validate_record(item, i))

    if all_errors:
        for line in all_errors:
            print(line, file=sys.stderr)
        return 1

    print(f"OK: {len(data)} event(s) passed structural checks.", file=sys.stderr)

    if args.dry_run:
        for i, item in enumerate(data):
            for kw in item.get("image_search_keywords", []):
                job = {
                    "event_index": i,
                    "date": item.get("date"),
                    "title": item.get("title"),
                    "keyword": kw,
                }
                print(json.dumps(job, ensure_ascii=False))
        return 0

    if args.search:
        # Normalize to mutable dicts
        rows: list[dict[str, Any]] = [dict(x) for x in data]
        run_web_image_search(
            rows,
            max_images=max(1, min(args.max_images, 10)),
            pause=max(0.0, args.pause),
            verify_head=args.verify_head,
            openverse=not args.no_openverse,
        )
        out_text = json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.write_text(out_text, encoding="utf-8")
            print(f"Wrote {args.output}", file=sys.stderr)
        else:
            sys.stdout.write(out_text)
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
