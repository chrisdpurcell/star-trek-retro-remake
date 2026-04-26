# ADR-0004 — TOML for save and config, never pickle or dill

**Status:** Accepted
**Date:** 2026-04-26

## Context

`pickle` and `dill` deserialization is arbitrary code execution by design — the format embeds Python opcodes that the unpickler runs. A malicious save file from any source (mod, downloaded share, untrusted USB drive) can root the player's machine on load. Even a single-user desktop game can be tricked into loading something it shouldn't. The risk is not theoretical: it is the documented threat model behind every "do not pickle untrusted data" warning in the Python standard library.

## Decision

All save game state and all configuration data is serialized through `pydantic` v2 models to TOML — `tomllib` for read, `tomli_w` for write. `pickle`, `dill`, `marshal`, and other code-executing serializers are forbidden in this codebase. The single exception is `QSettings` INI for window/dock geometry (binary `QByteArray` doesn't fit cleanly in TOML), which contains no game state and no user-supplied data.

## Consequences

- Save files are human-readable and human-editable, which is also useful during debugging.
- `pydantic` validates at load time, so malformed data crashes at the schema boundary rather than deep in turn logic. Mod authors get useful error messages.
- A small write-time cost for serialization vs. pickle, but `pydantic` v2's Rust core makes this negligible relative to disk I/O.
- Rejected alternative: pickle for speed plus signature verification. Rejected because the signature has to live somewhere the user can't tamper with — which doesn't exist on a single-user desktop.

See `docs/design/DESIGN.md` §9.5 "Saved-State Security" and §9.2 library table.
