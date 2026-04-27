# Data model — history highlights

The app stores **highlight** records (historical events, birthdays, culture hooks, and similar “on this day” items). Each document (or row) follows the shape below. Machine-readable validation lives in [schema/event.schema.json](../schema/event.schema.json); a filled sample array is in [schema/schema.json](../schema/schema.json).

## Canonical storage vs display

- **`date`** (required): **ISO 8601 calendar date** `YYYY-MM-DD` — the historical day for the story (e.g. event date, or a person’s birth date on that month-day in their birth year).
- **Localized labels** (e.g. `4月20日`): derive in the **frontend** from `date` and locale, or optionally store `locale_calendar_label` for ingest/debug.

## Event record

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| `date` | string (ISO date) | yes | Calendar date for the highlight |
| `category` | string | yes | UI grouping (e.g. 政治・行政, 人物・生誕と命日) |
| `highlight_kind` | string | no | Editorial tag: `event`, `birthday`, `death_anniversary`, `culture`, `other` |
| `title` | string | yes | Main headline |
| `subtitle` | string | no | Secondary line |
| `summary` | string | no | Short overview |
| `description` | string (long text) | yes | Main body copy |
| `image_search_keywords` | array of string | yes | **3–10** short queries for the [image-search-pipeline](../image-search-pipeline/) — **no URLs** |
| `images` | array of string (URI) | no | Resolved image URLs or paths; usually **empty at ChatGPT ingest**, filled by the image pipeline |
| `year` | string | no | Legacy ingest helper (e.g. `2004年`); prefer deriving from `date` |
| `locale_calendar_label` | string | no | Optional ingest helper |
| `source_run_id` | string | no | Batch / idempotency for re-ingestion |

## JSON shape (canonical)

```json
{
  "date": "2004-04-20",
  "category": "政治・行政",
  "highlight_kind": "event",
  "title": "（見出し）",
  "subtitle": "（補足）",
  "summary": "（短い概要）",
  "description": "（本文）",
  "image_search_keywords": [
    "2004年 年金改革 国会 写真",
    "小泉純一郎 内閣 記者会見 画像",
    "日本 社会保障 2004 ニュース 資料"
  ],
  "images": []
}
```

## Relational mapping (optional)

- **events**: core columns including `description`, optional `highlight_kind`.
- **event_image_search_keywords**: `event_id`, `sort_order`, `query` (normalized from JSON array), or store as JSON in a single column.
- **event_images**: `event_id`, `url` or `path`, `sort_order` — populated after the image-search pipeline.

## Suggested indexes

- Index on `date` for “on this day” lookups.
- Index on `category` and optional `highlight_kind` if you filter in the API.
