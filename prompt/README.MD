# Ingestion prompts (ChatGPT.com)

Research runs use **chatgpt.com** in the browser (optionally with **web search** enabled), not the OpenAI API. Output is then **parsed** into canonical JSON and validated before database load.

## Artifacts

| File | Role |
|------|------|
| [daily-events.template.md](daily-events.template.md) | Copy-paste prompt for one calendar day |
| [../schema/event.schema.json](../schema/event.schema.json) | Target shape for parser output |
| [../docs/data-pipeline.md](../docs/data-pipeline.md) | End-to-end pipeline and risks |

## Expected model output

Prefer a **single fenced JSON code block** containing an **array of objects**, each object matching the schema (field names exactly: `date`, `category`, `title`, `subtitle`, `summary`, `description`, `images`, optional `locale_calendar_label`, optional `year` for ingest only).

If the model returns Markdown sections instead, the parser must still emit valid JSON for validation.

## Acquisition (team standard)

Document the method you adopt and keep it stable:

1. **Recommended baseline**: Manual copy of the assistant message into a raw text file, then run the parser CLI/script (to be implemented in the backend or tooling repo).
2. **Automation** (optional): Any DOM or network automation against chatgpt.com requires **legal/compliance review** and owner maintenance when the UI changes.

## Parser ownership

Assign a **named owner** in [../docs/team.md](../docs/team.md) for: prompt versioning, parser code location (linked repo), validation failures, and re-ingestion playbooks.

## Versioning

When the prompt or schema changes, bump a **prompt version** string inside `daily-events.template.md` and record the change in [../docs/progress.md](../docs/progress.md) or your issue tracker.
