import pytest
from backend.app.db.session import engine

def test_db_engine_creation():
    # Just a simple test to ensure engine is created and URL is populated
    assert engine is not None
    assert str(engine.url).startswith("mysql")
