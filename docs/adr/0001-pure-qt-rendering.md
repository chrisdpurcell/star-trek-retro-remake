---
schema_version: '1.1'
id: 'adr-0001-star-trek-retro-remake-pure-qt-rendering'
title: 'Pure-Qt rendering, no pygame or SDL'
description: 'Decision to use Qt exclusively for rendering and avoid pygame and SDL.'
doc_type: 'adr'
status: 'active'
created: '2026-04-26'
updated: '2026-07-26'
reviewed: null
owner: 'project-maintainer'
consumer: 'mix'
tags:
  - 'adr'
  - 'architecture'
  - 'decision'
aliases: []
related: []
source: []
confidence: 'unknown'
visibility: 'public'
license: null
---

# ADR-0001 — Pure-Qt rendering, no pygame or SDL

**Status:** Accepted **Date:** 2026-04-26

## Context

The earlier v0.0.x prototype used `pygame-ce` for rendering inside a windowed PySide6 host, which required `libsdl2-dev` as a system dependency, dual event-loop bridging between Qt and SDL, and the SDL window-embedding hack. The integration friction was the largest single source of bugs in the prototype. See `docs/design/tech-stack-pyside6.md` §1 for the full rationale.

## Decision

All rendering — including the isometric sector map — uses Qt's `QGraphicsView` and `QGraphicsScene` exclusively. No `pygame`, `pygame-ce`, SDL, or any other rendering backend is permitted. The application runs on a single Qt event loop.

## Consequences

- One framework, one event loop, one input pipeline — eliminates the dual-loop bridging code that caused the prototype's worst bugs.
- `QGraphicsView` provides item-based 2D scene management, hit testing, transforms, and z-ordering natively; the turn-based game does not need pygame's frame-driven rendering model.
- No `libsdl2-dev` system dependency. Standard Qt6 system libs come with the `PySide6` wheel, simplifying both dev setup and AppImage packaging.
- Rejected alternative: keep `pygame-ce` for the map and use Qt only for chrome. Rejected because the integration friction does not get smaller as the game grows.

See `docs/design/DESIGN.md` §9.1 and `docs/design/tech-stack-pyside6.md` §1, §3.
