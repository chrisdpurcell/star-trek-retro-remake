from __future__ import annotations


def test_import_stmrr() -> None:
    import stmrr  # noqa: F401


def test_version_present() -> None:
    import stmrr

    assert stmrr.__version__
