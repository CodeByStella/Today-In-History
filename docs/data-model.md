# Data model — history events

The app stores **history event** records. Each document (or row) follows the shape below. Machine-readable validation lives in [schema/event.schema.json](../schema/event.schema.json); a filled sample array is in [schema/schema.json](../schema/schema.json).

## Canonical storage vs display

- **`date`** (required): **ISO 8601 calendar date** of the historical event, `YYYY-MM-DD`. This is the single source of truth for sorting and “on this day” queries.
- **Localized labels** (for example `4月20日`): derive in the **frontend** from `date` and locale, or optionally store a duplicate in `locale_calendar_label` for ingest/debug — not required for the app.

## Event record

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| `date` | string (ISO 8601 date) | yes | Calendar date for the event (e.g. `1999-12-31`, format `YYYY-MM-DD`) |
| `category` | string | yes | Category label for filtering and grouping (used when showing events by category) |
| `title` | string | yes | Main headline for the event |
| `subtitle` | string | no | Optional secondary line (e.g. year, location, or short tagline) |
| `summary` | string | no | Short overview (one or two sentences) |
| `description` | string (long text) | yes | Full narrative, explanation, or long summary text |
| `images` | array of string (URI) | no | Image URLs or paths; use an empty array when there are no images |
| `year` | string | no | **Legacy / ingest helper** only (e.g. `2004年`); prefer deriving year from `date` |
| `locale_calendar_label` | string | no | Optional display helper from ingest (e.g. `4月20日`); not required if UI formats `date` |
| `source_run_id` | string | no | Optional idempotency / provenance for re-ingestion batches |

## JSON shape (canonical)

```json
{
  "date": "2004-04-20",
  "category": "政治・行政",
  "title": "（イベントの見出し）",
  "subtitle": "（補足・副題）",
  "summary": "（短い概要。1〜2文）",
  "description": "（説明文の本文。複数文可）",
  "images": []
}
```

## Example (filled)

```json
{
  "date": "2004-04-20",
  "category": "政治・行政",
  "title": "年金制度改革法成立",
  "subtitle": "持続可能性を巡る大転換",
  "summary": "少子高齢化に対応するための年金制度改革法が成立。",
  "description": "小泉内閣のもとで成立したこの改革では、保険料の段階的引き上げと給付抑制が導入された。将来世代への負担軽減と制度維持を目的としたが、国民の不安や批判も大きく、以後の社会保障議論の軸となった。",
  "images": [],
  "locale_calendar_label": "4月20日"
}
```

## Relational mapping (optional)

If you use a SQL database with a normalized `images` table:

- **events**: `id`, `date`, `category`, `title`, `subtitle`, `summary`, `description` (plus `created_at` / `updated_at` if you need them).
- **event_images**: `id`, `event_id` (foreign key to `events`), `url` (or `path`), optional `sort_order`.

The document model is equivalent to one event row plus its related image rows or URLs.

## Suggested indexes

- Primary key (or unique id) on `id` if you use surrogate keys.
- Index on `date` for “on this day” lookups.
- Index on `category` if you often filter or group by category.
