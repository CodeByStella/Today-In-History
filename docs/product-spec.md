# Product specification — content and output rules

This app answers “what happened in history on this day?” (for example, **April 20** or any calendar date you query). The dataset focuses on **important events in modern Japanese history**, grouped for display and storage as described below.

For product direction and MVP scope, see [product-strategy.md](product-strategy.md). For persisted record shape, see [data-model.md](data-model.md).

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

## Mapping to the data schema

| Concept | Field(s) to use |
|---------|-----------------|
| Year | Primary: derive from `date` (`YYYY-MM-DD`). Optional: `subtitle` or legacy `year` during migration |
| Title | `title` |
| Overview / short summary | `summary`, or `subtitle`, or the opening of `description` |
| Image(s) | `images` (array of URL or file path strings) |
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
