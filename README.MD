# Today in History — program hub

This repository is the **program hub** for the Today in History product: it holds specifications, data contracts, prompts, UI mocks, strategy notes, and links to application code in **other repositories**. It is **not** the primary home for production app source, CI secrets, or deployed API keys.

## Repository structure

| Path | Contents |
|------|----------|
| [registry.json](registry.json) | Index of artifacts in this hub (schemas, mocks, prompts, docs, linked repos). Start here for a machine-readable catalog. |
| [docs/](docs/) | Narrative documentation: pipeline, data model, product spec, strategy, team template, progress. |
| [schema/](schema/) | JSON Schema (`event.schema.json`) and sample data (`schema.json`). |
| [prompt/](prompt/) | ChatGPT.com ingestion prompts and how to run the editorial pipeline. |
| [mock/](mock/) | Static UI prototypes; see below for the hosted preview. |

## Where to find what

| Topic | Location |
|--------|----------|
| **Live UI mock** (GitHub Pages) | [https://codebystella.github.io/Today-In-History/mock/first/](https://codebystella.github.io/Today-In-History/mock/first/) — same assets as [mock/first/](mock/first/) |
| Content rules (scope, categories, volume, field mapping) | [docs/product-spec.md](docs/product-spec.md) |
| Event record fields, JSON examples, SQL sketch, indexes | [docs/data-model.md](docs/data-model.md) |
| Formal JSON Schema (one event) | [schema/event.schema.json](schema/event.schema.json) |
| Sample event array | [schema/schema.json](schema/schema.json) |
| Ingestion: ChatGPT.com → parse → DB | [docs/data-pipeline.md](docs/data-pipeline.md) |
| Prompt templates | [prompt/](prompt/) |
| Product vision and MVP | [docs/product-strategy.md](docs/product-strategy.md) |
| Monetization notes | [docs/monetization.md](docs/monetization.md) |
| Roles / parser ownership template | [docs/team.md](docs/team.md) |
| Delivery tracking pointers | [docs/progress.md](docs/progress.md) |

## Linked application repositories

URLs live in [registry.json](registry.json) under `external_repositories` (frontend, backend). Replace `null` values when those repos exist.
