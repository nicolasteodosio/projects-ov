from datetime import datetime

from database.db_connection import db
from pony.orm import PrimaryKey, Required, Set


class Participants(db.Entity):
    id = PrimaryKey(int, auto=True)
    employee_id = Required(str)
    full_name = Required(str)
    department = Required(str)
    is_owner = Required(bool)
    created_at = Required(datetime)
    project = Set("Projects")
