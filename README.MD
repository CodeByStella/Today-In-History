# Today in history

This app answers “what happened in history on this day?” (for example, **April 20** or any calendar date you query). The dataset focuses on **important events in modern Japanese history**, grouped for display and storage as described below.

## Output requirements (command spec)

When a date is requested, the output should follow these rules.

**Summary**

| Rule | Description |
|------|-------------|
| **Scope** | Important events in **modern Japanese history** |
| **Order** | **Newest first** by year (most recent year at the top). *Note: the source line used a Japanese phrase that we interpret as this sort order; if you use a different rule, update this table.* |
| **Layout** | **Split by category** — each category is its own block of events |
| **Volume** | **3–5 events per category** |
| **Media** | Each event can have **related image(s)** |
| **Per-event fields** | **Year**, **title**, **brief summary (overview)**, **image(s)**, and **longer description (explanation)** |

**Mapping to the data schema (recommended)**

| Concept | Field(s) to use |
|---------|-----------------|
| Year | Derive from `date`, or show the year in `subtitle` for display only |
| Title | `title` |
| Overview / short summary | `subtitle`, or the opening of `description` |
| Image(s) | `images` (array of URL or file path strings) |
| Full explanation | `description` (main body) |

**Original specification (Japanese)**

```text
歴史の中の今日、（4月20日）。
日本現代史の重要なイベントを出力します。
情熱方式は最新順にします。
カテゴリ別にイベントを分割して出力します。
各イベントに関連する画像があります。
各カテゴリには3〜5個のデータがあります。
各イベントデータには、年、タイトル、概要、画像、説明が含まれます。
```

---

# Database data schema

The app stores **history event** records. Each document (or row) follows this shape.

## Event record

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| `date` | string (ISO 8601 date) | yes | Calendar date for the event (e.g. `1999-12-31`, format `YYYY-MM-DD`) |
| `category` | string | yes | Category label for filtering and grouping (used when showing events by category) |
| `title` | string | yes | Main headline for the event |
| `subtitle` | string | no | Optional secondary line (e.g. year, location, or short tagline) |
| `description` | string (long text) | yes | Full narrative, explanation, or long summary text |
| `images` | array of string (URI) | no | Image URLs or paths; use an empty array when there are no images |

### JSON shape

```json
{
  "date": "",
  "year":"",
  "category": "",
  "title": "",
  "subtitle": "",
  "summary" : "",
  "description": "",
  "images": []
}
```

### Example (filled)

```json
{
  "date": "1969-07-20",
  "category": "Space",
  "title": "First humans on the Moon",
  "subtitle": "Apollo 11",
  "description": "Neil Armstrong and Buzz Aldrin landed the Lunar Module Eagle in the Sea of Tranquility.",
  "images": ["https://example.org/apollo11.jpg"]
}
```

### Relational mapping (optional)

If you use a SQL database with a normalized `images` table:

- **events**: `id`, `date`, `category`, `title`, `subtitle`, `description` (plus `created_at` / `updated_at` if you need them).
- **event_images**: `id`, `event_id` (foreign key to `events`), `url` (or `path`), optional `sort_order`.

The document model is equivalent to one event row plus its related image rows or URLs.

### Suggested indexes

- Primary key (or unique id) on `id` if you use surrogate keys.
- Index on `date` for “on this day” lookups.
- Index on `category` if you often filter or group by category.
