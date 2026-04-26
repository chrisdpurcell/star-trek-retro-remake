# Star Trek Retro Remake

A turn-based, grid-based Star Trek strategy game inspired by *Star Trek* (1971) and *Super Star Trek* (1973), reimagined with a windowed graphical interface that evokes mid-1990s desktop strategy games — *Master of Orion 2*, *X-COM: UFO Defense*, *Heroes of Might and Magic 2*.

> **Status:** Pre-scaffold. Game design is locked in [`DESIGN.md`](DESIGN.md); source code does not yet exist. The first build will be `v0.1`.

## At a glance

- **Platform:** Linux only. No Windows or macOS support planned.
- **Language:** Python 3.14+
- **UI / rendering:** PySide6 (Qt 6.5+), single event loop, `QGraphicsView` for the isometric map
- **Distribution:** AppImage at v1.0; `uv` for development
- **Aesthetic:** windowed application with chunky bevels, dock panels, monospace info displays, isometric grid with z-levels

## Disclaimer

This is an unofficial, non-commercial fan project. *Star Trek* and all related marks, characters, ships, and concepts are intellectual property of CBS Studios Inc. / Paramount Global, including trademarks and copyrights. This project is not affiliated with, endorsed by, or sponsored by CBS Studios or Paramount.

Visual assets are AI-generated (OpenAI ChatGPT Images 2.0). Prompts are archived per-asset for provenance — see `assets/prompts/` once the asset pipeline is in place.

## Documents

- [`DESIGN.md`](DESIGN.md) — canonical Game Design Document (gameplay, world, mechanics, technical architecture)
- [`tech-stack-pyside6.md`](tech-stack-pyside6.md) — scaffold-phase operational notes
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — coding standards and contribution workflow
- [`SECURITY.md`](SECURITY.md) — vulnerability reporting
- [`NOTICE.md`](NOTICE.md) — IP boundary and bundled-asset licenses
- [`CHANGELOG.md`](CHANGELOG.md) — release history

## License

Code is licensed under [MIT](LICENSE). The Star Trek IP referenced in this project is *not* licensed by the MIT grant — see [`NOTICE.md`](NOTICE.md).

## Inspiration

- *Star Trek* (Mike Mayfield, 1971)
- *Super Star Trek* (David Ahl, 1973)
- *Star Trek: 25th Anniversary* (1992)
- *Star Trek: Starfleet Command* series
