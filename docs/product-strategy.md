# Product strategy (draft)

## Vision

Help users explore **what happened on this calendar day** in history, with a calm, readable experience and **trustworthy** Japanese modern-history storytelling.

## Audience (initial hypothesis)

- Readers interested in **Japan** (residents, diaspora, students).
- Casual daily open: one screen, scannable categories, optional depth in `description`.

## Differentiation

- **Curated scope:** modern Japanese history with explicit category blocks and consistent volume (see [product-spec.md](product-spec.md)).
- **Owned dataset:** built through a documented pipeline ([data-pipeline.md](data-pipeline.md)), not only third-party APIs at runtime.

## MVP scope

- **One day type:** “on this day” for month-day, backed by canonical event JSON.
- **Locales:** Japanese UI copy with data in Japanese; date formatting per device locale later.
- **Media:** ChatGPT outputs **`image_search_keywords`** only; **`images`** are filled by the hub **image-search-pipeline** (or downstream) after URL verification and rights checks; empty `images` remains acceptable if no safe asset is found.

## Non-goals (for early releases)

- Real-time news.
- User-generated history articles without moderation.
- Scraping chatgpt.com from end-user devices (ingestion is an **internal** publishing step).

## Dependencies

- Linked **frontend** and **backend** repositories (see [registry.json](../registry.json) `external_repositories`) once created.
- JSON Schema and sample data in [schema/](../schema/) as the contract between ingestion and app.
