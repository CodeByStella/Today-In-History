# Team (template)

Fill in as the core team forms. This hub stays lightweight; detailed HR data belongs elsewhere.

| Role | Name | Contact | Notes |
|------|------|---------|-------|
| Product owner | | | Scope and prioritization |
| Engineering lead | | | Linked app repos, release process |
| Content / editorial | | | Prompt quality, factual review |
| Design | | | Mock handoff from `mock/` |
| Ingestion / data | | | Parser owner; see [prompt/README.MD](../prompt/README.MD) |

## Decision rights

- **Schema changes** (`schema/event.schema.json`): require product + engineering sign-off; version prompts accordingly.
- **Pipeline changes** ([data-pipeline.md](data-pipeline.md)): ingestion owner + compliance if automation touches chatgpt.com.
