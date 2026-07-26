from __future__ import annotations


def test_import_stmrr() -> None:
    import stmrr

    assert stmrr.__name__ == "stmrr"


def test_version_present() -> None:
    import stmrr

    assert stmrr.__version__
