import os

from pony import orm

db = orm.Database()

if os.getenv("TESTING", False):
    db.bind("sqlite", ":memory:")
else:
    db.bind(
        provider="mysql",
        host=os.getenv("MARIADB_HOST"),
        port=3306,
        user=os.getenv("MARIADB_USER"),
        passwd=os.getenv("MARIADB_PASSWD"),
        db=os.getenv("MARIADB_DATABASE"),
    )
