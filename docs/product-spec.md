# Product specification — content and output rules

This app answers “what happened in history on this day?” (for example, **April 20** or any calendar date you query). The dataset focuses on **engaging highlights in and around modern Japan**—not only political events but also **birthdays, anniversaries, and culture hooks** when they are well-sourced and interesting to a general reader. Grouping and storage follow the rules below.

For product direction and MVP scope, see [product-strategy.md](product-strategy.md). For persisted record shape, see [data-model.md](data-model.md).

## Output requirements (command spec)

When a date is requested, the output should follow these rules.

**Summary**

| Rule | Description |
|------|-------------|
| **Scope** | **Modern Japan–centric “today” highlights**: major events plus **birthdays, deaths, culture** items when sourced and engaging |
| **Order** | **Newest first** by year within each category (most recent `date` year at the top). *If you change sort rules, update this table.* |
| **Layout** | **Split by category** — each category is its own block |
| **Volume** | **About 2–5 items per category** when material exists (see prompt for soft totals) |
| **Media** | ChatGPT supplies **`image_search_keywords` only**; **[`image-search-pipeline/`](../image-search-pipeline/)** resolves **`images`** for the app |
| **Per-event fields** | **Date**, **title**, **overview** (`summary` / `subtitle`), **long body** (`description`), **keywords → images** |

## Mapping to the data schema

| Concept | Field(s) to use |
|---------|-----------------|
| Year | Primary: derive from `date` (`YYYY-MM-DD`). Optional: `subtitle` or legacy `year` during migration |
| Title | `title` |
| Overview / short summary | `summary`, or `subtitle`, or the opening of `description` |
| Image discovery | `image_search_keywords` (string array for the pipeline) |
| Image delivery | `images` (URLs or paths **after** the image-search pipeline) |
| Full explanation | `description` (main body) |

## Original specification (Japanese)

```text
歴史の中の今日、（4月20日）。
日本現代史の重要なイベントを出力します。
情熱方式は最新順にします。
カテゴリ別にイベントを分割して出力します。
各イベントに関連する画像があります。
各カテゴリには3〜5個のデータがあります。
各イベントデータには、年、タイトル、概要、画像、説明が含まれます。
```

*Operational note:* the live pipeline separates **copy** (ChatGPT) from **pixels** (`image_search_keywords` → `image-search-pipeline` → `images`). The Japanese lines above remain the spirit of the product; “画像” is satisfied by resolved URLs after the pipeline, not by the LLM inventing links.
