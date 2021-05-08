from datetime import datetime

from database.db_connection import db
from pony.orm import Optional, PrimaryKey, Required, Set


class Projects(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    state = Required(str)
    participants = Set("Participants")
    progress = Optional(float)
    created_at = Required(datetime)
