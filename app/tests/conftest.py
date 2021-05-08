import pytest


@pytest.fixture(autouse=True)
def clear_database():
    from database.db_connection import db

    if db.provider_name != "sqlite":
        raise RuntimeError("Not running tests on sqlite. Check your configuration.")

    if not db.entities:
        # No models imported, so no tables to drop/recreate
        return

    db.drop_all_tables(with_all_data=True)
    db.create_tables()
