---
schema_version: '1.1'
id: 'index-pgjfi7-star-trek-retro-remake'
title: 'Star Trek Retro Remake'
description: 'Project overview, current status, platform, documentation, licensing, and inspiration for Star Trek Retro Remake.'
doc_type: 'index'
status: 'active'
created: '2026-04-26'
updated: '2026-07-26'
reviewed: null
owner: 'project-maintainer'
consumer: 'mix'
tags:
  - 'index'
aliases: []
related: []
source: []
confidence: 'unknown'
visibility: 'public'
license: null
---

# Star Trek Retro Remake

A turn-based, grid-based Star Trek strategy game inspired by _Star Trek_ (1971) and _Super Star Trek_ (1973), reimagined with a windowed graphical interface that evokes mid-1990s desktop strategy games — _Master of Orion 2_, _X-COM: UFO Defense_, _Heroes of Might and Magic 2_.

> **Status:** v0.1 scaffold in progress. Steps 1–10 are complete, including the Qt-free model, state/event pipeline, controller bridge, main window, and runnable application shell. Step 11 (`MapView` and `GridScene`) is next. Game design is locked in [`docs/design/DESIGN.md`](docs/design/DESIGN.md); live state is in [`docs/handoff/state.md`](docs/handoff/state.md).

## At a glance

- **Platform:** Linux only. No Windows or macOS support planned.
- **Language:** Python 3.14+
- **UI / rendering:** PySide6 (Qt 6.5+), single event loop, `QGraphicsView` for the isometric map
- **Distribution:** AppImage at v1.0; `uv` for development
- **Aesthetic:** windowed application with chunky bevels, dock panels, monospace info displays, isometric grid with z-levels

## Disclaimer

This is an unofficial, non-commercial fan project. _Star Trek_ and all related marks, characters, ships, and concepts are intellectual property of CBS Studios Inc. / Paramount Global, including trademarks and copyrights. This project is not affiliated with, endorsed by, or sponsored by CBS Studios or Paramount.

Visual assets are AI-generated (OpenAI ChatGPT Images 2.0). Prompts are archived per-asset for provenance — see `assets/prompts/` once the asset pipeline is in place.

## Documents

- [`docs/design/DESIGN.md`](docs/design/DESIGN.md) — canonical Game Design Document (gameplay, world, mechanics, technical architecture)
- [`docs/design/tech-stack-pyside6.md`](docs/design/tech-stack-pyside6.md) — scaffold-phase operational notes
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — coding standards and contribution workflow
- [`SECURITY.md`](SECURITY.md) — vulnerability reporting
- [`NOTICE.md`](NOTICE.md) — IP boundary and bundled-asset licenses
- [`CHANGELOG.md`](CHANGELOG.md) — release history

## License

Code is licensed under [MIT](LICENSE). The Star Trek IP referenced in this project is _not_ licensed by the MIT grant — see [`NOTICE.md`](NOTICE.md).

## Inspiration

- _Star Trek_ (Mike Mayfield, 1971)
- _Super Star Trek_ (David Ahl, 1973)
- _Star Trek: 25th Anniversary_ (1992)
- _Star Trek: Starfleet Command_ series
