# Markdown Frontmatter Standard: Agent Summary

The canonical [Markdown Frontmatter 1.5 standard](https://github.com/L3DigitalNet/project-standards/blob/v5/standards/markdown-frontmatter/versions/1.5/README.md) is authoritative and wins if this summary conflicts with it.

Lifecycle: active. Package: `markdown-frontmatter@1.5`.

## Use this summary when

Add, repair, or validate metadata on Markdown paths selected by the `markdown-frontmatter` package options in `.standards/config.toml`.

## Core rules

- Every managed document has the eleven minimal fields in canonical order: `schema_version`, `id`, `title`, `description`, `doc_type`, `status`, `created`, `updated`, `tags`, `aliases`, and `related`. Most project docs use the richer standard profile.
- Quote strings and dates. Both quote forms are accepted; Prettier's minimal-escape resting state is the converged form, so legacy single-quoted spellings stay valid. Use block-style non-empty lists with quoted items and `[]` for empty lists. Reject duplicate list items and unknown top-level fields; extensions belong under `publish`, `project`, or `x_project`.
- Ordinary IDs are `{doc_type}-{six-character-base36-token}-{frozen-kebab-slug}`. ADR IDs are `adr-NNNN-repo-name-short-title`. Generate ordinary IDs with tooling.
- Structure rules define schema, order, syntax, and ID shape. Field-value policy defines lifecycle, ownership, tags, relationships, confidence, visibility, and repository-local vocabulary; adopters should record that policy in an ADR.
- Never add managed-document frontmatter to `CLAUDE.md`, `AGENTS.md`, `.claude/**`, `.agents/**`, or `.codex/**`; exclude those harness files from managed scope.

## Commands and artifacts

```bash
project-standards validate
format-frontmatter --check
validate-id
validate-references
```

The aggregate validator covers schema, ID, and enabled reference checks. `format-frontmatter` checks or fixes canonical source style. The repo-local skill at `.agents/skills/markdown-frontmatter/SKILL.md` guides authoring and ID generation.

## Boundaries and companions

This standard governs metadata, not Markdown body formatting. Markdown Tooling is a companion. ADR is a companion document profile; neither relation silently changes adoption behavior.

## Canonical resources

Use the [versioned package documentation](https://github.com/L3DigitalNet/project-standards/tree/v5/standards/markdown-frontmatter/versions/1.5) for complete requirements.
