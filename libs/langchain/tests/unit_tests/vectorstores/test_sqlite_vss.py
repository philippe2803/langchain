import sqlite3
import pytest


@pytest.mark.requires("sqlite-vss")
def test_sqlite_load_extension():
    db = sqlite3.connect(':memory:')
    db.enable_load_extension(True)
    sqlite_vss.load(db)
    db.enable_load_extension(False)
    version = db.execute('select vss_version()').fetchone()
    assert version is not None
