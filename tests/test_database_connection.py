from ..database import engine, test_engine

def test_db_connection():
    assert engine.connect()
    
def test_tdb_connection():
    assert test_engine.connect()
