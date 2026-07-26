---
name: markdown-frontmatter
description: Use when adding, fixing, or validating YAML frontmatter on managed Markdown governed by the project-standards Markdown Frontmatter Standard; covers structure, field values, id generation, and validation.
compatibility: Claude Code and Codex CLI
license: MIT
metadata:
  author: Chris Purcell
  version: '1.4'
---

# Markdown Frontmatter

## Overview

Author and fix YAML frontmatter for **managed Markdown documents** under the [project-standards Markdown Frontmatter Standard](https://github.com/L3DigitalNet/project-standards/blob/main/standards/markdown-frontmatter/README.md).

This skill ships with the standard package and is installed repo-local at `.agents/skills/markdown-frontmatter` when a repository adopts the standard. That path is deliberate: both Claude Code and Codex CLI can discover it without a global skill owner.

**Core principle: the schema is authoritative, not this file.** The machine contract is `markdown-frontmatter.schema.json` in project-standards, enforced by `project-standards validate`. This skill is the operating layer for the rules agents get wrong most often. On any conflict, the schema and current standard pages win.

## When to use

- Creating or editing a managed Markdown file (typically `README.md`, `docs/**/*.md`).
- A `project-standards validate`, `validate-frontmatter`, or `format-frontmatter --check` run failed and you need to fix the block.
- Deciding which `doc_type` / `status` / other controlled value to set.

**When NOT to use: files that must NEVER carry frontmatter.** Agent-instruction and agent-skill files are harness config, not managed documents: `CLAUDE.md`, `AGENTS.md`, and anything under `.claude/`, `.agents/`, `.codex/`. That includes this installed skill at `.agents/skills/markdown-frontmatter`. Exclude those paths through the package's `exclude` option in `.standards/config.toml` instead of adding metadata. A repo may also exclude its root `README.md` if it prefers no metadata table on its landing page.

## Required fields (the eleven)

Every managed document opens with a `---` fenced YAML block carrying at least these, in this order:

```yaml
---
schema_version: '1.1'
id: 'note-xxxxxx-human-title'
title: 'Human Title'
description: 'One-sentence description of the document.'
doc_type: 'note'
status: 'draft'
created: 'YYYY-MM-DD'
updated: 'YYYY-MM-DD'
tags: []
aliases: []
related: []
---
```

For most docs, add the standard-profile optionals after `updated` in canonical order: `reviewed` (date|null), `owner` (stable person/team/role), `consumer` (enum), then after `related`: `source` (array), `confidence` (enum), `visibility` (enum), `license` (string|null). Relationship fields are optional, used only when needed: `supersedes`, `superseded_by`, `depends_on`, `applies_to`.

## Formatting rules that actually fail validation

These are the machine-checked rules an agent skips by habit:

- **Quote every string, including dates.** `created: '2026-06-07'`, never `created: 2026-06-07`.
- **Identifier-like numbers are strings.** `schema_version: '1.1'`, not `1.1`.
- **Non-empty lists use block style** (`- 'item'` per line); **empty lists use `[]`**. No duplicate items.
- **No unknown top-level fields.** A stray `version:` or `type:` is rejected. Project- or tool-specific keys go under the `publish`, `project`, or `x_project` extension objects only.
- **Canonical key order** when keys are present:

  ```text
  schema_version, id, title, description, doc_type, status, created, updated,
  reviewed, owner, consumer, tags, aliases, related, supersedes, superseded_by,
  depends_on, applies_to, source, confidence, visibility, license,
  publish, project, x_project
  ```

## Controlled values

These fields accept only these values (the schema is the source of truth):

| Field | Allowed values |
| --- | --- |
| `doc_type` | `index`, `note`, `concept`, `reference`, `runbook`, `spec`, `plan`, `adr`, `decision`, `research`, `template`, `log`, `prompt`, `schema` |
| `status` | `draft`, `active`, `review`, `deprecated`, `archived`, `superseded`, `stub` |
| `confidence` | `high`, `medium`, `low`, `unknown` |
| `visibility` | `private`, `internal`, `public` |
| `consumer` | `user`, `agent`, `mix`, `unknown` |

- `README.md` and `index.md` → `doc_type: 'index'`. Files under `docs/research/` → `doc_type: 'research'`.
- `stub` is a **status**, never a `doc_type`. Use `doc_type`, never `type`.
- Canonical global tags include `frontmatter`, `metadata`, `standard`, `validation`, `infrastructure`, `it`, and `network`; repos may add documented local tags when the global set is insufficient.

## The `id` field — standard-enforced format

> **This is a standard rule, not a local addition.** `markdown-frontmatter@1.5` enforces the id format below via `validate-id` (run by `project-standards validate` and the V5 CI workflow). An id whose leading segment is not a valid `doc_type` **fails validation** with `prefix '<x>' is not a valid doc_type`. Earlier repo-name-prefixed ids no longer pass.

```text
{doc_type}-{base36-6}-{document-name}
```

The `doc_type` (one of the controlled values above), then a random 6-character base36 token, then a readable document slug, all lower kebab-case (e.g. `runbook-0f943i-restart-netbox-after-config-change`). The token keeps the id globally unique; the slug is frozen at creation and does **not** change when the title is edited.

**Generate the id with the script. Never invent the token yourself.** An LLM asked for a "random" base36 token produces low-entropy, collision-prone strings and reuses tokens already in context, defeating the uniqueness goal. `scripts/` is this skill's own directory (invoke by absolute path if your cwd is elsewhere):

```bash
scripts/new-doc-id <document-name>                        # bare id, doc_type 'note'
scripts/new-doc-id --doc-type runbook <document-name>     # bare id, 'runbook' prefix
scripts/new-doc-id --scaffold --doc-type runbook <name>   # full canonical frontmatter block
```

The `--doc-type` value becomes both the id prefix and (in `--scaffold`) the `doc_type` field, so the two always agree; it defaults to `note`. `--doc-type` and `--status` must be standard-controlled values. `--scaffold` emits the eleven required fields in canonical order with today's date correctly quoted. Replace the `REPLACE:` description placeholder before committing.

ADRs are the exception: follow the standard's ADR id form (`adr-{NNNN}-{repo-name}-{title}`, e.g. `adr-0001-homelab-use-postgresql-for-persistent-storage`), not the `doc_type`-prefixed format. Do not use the script for ADR ids.

## Worked example (compliant standard profile)

```yaml
---
schema_version: '1.1'
id: 'runbook-0f943i-restart-netbox-after-config-change'
title: 'Restart netbox after config change'
description: 'Procedure to safely reload netbox after editing its configuration.'
doc_type: 'runbook'
status: 'active'
created: '2026-03-10'
updated: '2026-06-07'
reviewed: '2026-06-07'
owner: 'platform-team'
consumer: 'user'
tags:
  - 'infrastructure'
  - 'network'
  - 'operations'
  - 'runbook'
aliases:
  - 'netbox-restart'
related:
  - 'docs/architecture.md'
source: []
confidence: 'high'
visibility: 'internal'
license: null
---
# Restart netbox after config change

...document body...
```

## Validate

Compliance = `project-standards validate` exits `0`. Run it from the repository root:

```bash
project-standards validate
```

That command runs schema validation, ID-format validation, and reference validation. Exit codes: `0` all matched files valid (or none matched); `1` one or more documents failed; `2` config/schema error.

Use the formatter check for canonical quote style, key order, and list layout:

```bash
format-frontmatter --check
```

To check or repair a single file's id: `validate-id <file>` (add `--fix` to rewrite an invalid id through the platform executor).

## Common mistakes

| Mistake | Fix |
| --- | --- |
| `type:` instead of `doc_type:` | Rename; `type` is not a field. |
| Unquoted date `created: 2026-06-07` | Quote it: `'2026-06-07'`. |
| `doc_type: 'readme'` for a README | README/index → `doc_type: 'index'`. |
| Extra top-level key (`version:`, `category:`) | Move under `project:`/`x_project:`, or drop it. |
| Frontmatter added to `CLAUDE.md` / `.claude/**` / `.agents/**` | Remove it; add the path to the package `exclude` option. |
| Omitting required arrays (`tags`/`aliases`/`related`) | Always present; empty = `[]`. |
| `doc_type: 'stub'` | `stub` is a `status`, not a `doc_type`. |

## Authoritative references

- [Standard README](https://github.com/L3DigitalNet/project-standards/blob/main/standards/markdown-frontmatter/README.md) — overview and adoption surface.
- [Structure Requirements](https://github.com/L3DigitalNet/project-standards/blob/main/standards/markdown-frontmatter/structure.md) — hard fields, key order, scalar/list rules, IDs, and validation.
- [Field Values](https://github.com/L3DigitalNet/project-standards/blob/main/standards/markdown-frontmatter/field-values.md) — lifecycle, ownership, canonical tags, aliases, relationships, sources, and extensions.
- [Adoption guide](https://github.com/L3DigitalNet/project-standards/blob/v5/standards/markdown-frontmatter/versions/1.5/adopt.md) — unified config, CI workflow, repo-local skill install, and compliance procedure.
- `standards/markdown-frontmatter/versions/1.5/schemas/markdown-frontmatter.schema.json` (in project-standards) — the selected package contract; wins on any conflict.
