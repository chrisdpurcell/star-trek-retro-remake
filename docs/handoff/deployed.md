# Deployed

**Status:** Nothing deployed. Pre-scaffold project.

This file becomes load-bearing once a runnable artifact exists (AppImage, dev-mode launch, or any continuously-running process). Until then it's a placeholder so the SessionStart hook's pointers don't 404.

## Target distribution (from `docs/design/tech-stack-pyside6.md` §8)

| Channel | When | Notes |
|---|---|---|
| Dev (`uv run python -m stmrr`) | Scaffold step 1 onward | Local-only. Bootstrapped via `uv python install 3.14`. |
| AppImage via `python-appimage` | v1.0 | Single-file Linux binary; bundles Python + PySide6 + game. |
| Flatpak | Future | Sandboxed alternative, not v1.0. |
| `.deb` via `dh-python` | Future | Native packaging. |
| PyPI | Never | This is a game, not a library. |

## Target system requirements

- Linux (Debian 13 / Ubuntu 24.04 LTS+)
- Wayland or X11 (PySide6 6.5+ handles both natively)
- No `libsdl2-dev` (pygame-ce dropped per `docs/design/tech-stack-pyside6.md` §1)
