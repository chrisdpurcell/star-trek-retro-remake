# Credentials

**Status:** No credentials in use. Pre-scaffold; no live services, no API integrations, no deployment endpoints.

This file becomes load-bearing once any of:

- An AI image-generation API key is needed for the asset pipeline (`docs/design/tech-stack-pyside6.md` §14). Likely path: `secret/api-keys/ai/openai`.
- A GitHub Actions deploy key or release-token is wired up (`docs/design/tech-stack-pyside6.md` §13.4 lists `.github/workflows/ci.yml` as a first-scaffold-push artifact).
- A signing key for AppImage releases is provisioned at v1.0.

OpenBao remains the source of truth. KV paths under `secret/api-keys/`, `secret/apps/`, `secret/ssh/`, `secret/gpg/` per the global credentials policy in `~/.claude/CLAUDE.md`.

## Format when populated

| Purpose | Bao path | Used by | Notes |
|---|---|---|---|
| (none yet) | | | |
