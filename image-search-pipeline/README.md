# Image search pipeline

Sub-project that turns **`image_search_keywords`** (from ChatGPT ingest) into **`images`** (HTTPS URLs) using **real web image search** over HTTP.

## What runs today

| Step | Implementation |
|------|----------------|
| Validate | `run.py` (stdlib): required fields, no URLs inside keywords |
| Keyword jobs | `run.py --dry-run` — one JSON line per keyword |
| **Image search** | `run.py --search` — **Wikimedia Commons** API (file search + `imageinfo`), then **Openverse** to fill remaining slots (CC-licensed Flickr/Wikimedia/etc. index). No API keys required for these two backends. |

**Caveats:** Commons search is literal; long Japanese queries often return few hits. Openverse improves recall but results are **CC-mixed** (Flickr, etc.)—check **license / attribution** before shipping in production. For Google Images–style precision, add a paid provider later (SerpAPI, Bing Image Search, Google Custom Search JSON) behind env vars.

## Contract

- **Input:** JSON array with `image_search_keywords` (3–10 strings per event). See [`schema/event.schema.json`](../schema/event.schema.json).
- **Output:** Same array with **`images`** set to up to N direct `https://` image URLs (`--max-images`, default 3).

## Run locally

Install **httpx** (required for `--search`):

```bash
cd image-search-pipeline
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate

python -m pip install -U pip
python -m pip install -r requirements.txt
```

**Commands**

```bash
# Structural validation only (no network)
python run.py -i events.json

# Print keyword jobs (no network)
python run.py -i events.json --dry-run

# Web image search → write enriched JSON (network)
python run.py -i events.json --search -o enriched.json

# stdout instead of -o
python run.py -i events.json --search > enriched.json

# Commons only (skip Openverse)
python run.py -i events.json --search --no-openverse -o out.json

# Optional: HTTP HEAD check each URL (slower)
python run.py -i events.json --search -o out.json --verify-head
```

**Flags:** `--max-images` (default 3), `--pause` delay between provider calls (default 0.35s), `--no-openverse`.

**Python:** 3.9+

## Files

| File | Purpose |
|------|---------|
| [`run.py`](run.py) | CLI: validate, `--dry-run`, `--search` |
| [`commons_provider.py`](commons_provider.py) | Wikimedia Commons API client |
| [`openverse_provider.py`](openverse_provider.py) | Openverse API fallback |
| [`requirements.txt`](requirements.txt) | `httpx` |

## Related docs

- [docs/data-pipeline.md](../docs/data-pipeline.md)
- [docs/data-model.md](../docs/data-model.md)
