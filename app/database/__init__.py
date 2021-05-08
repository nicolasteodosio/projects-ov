from database.db_connection import db
from database.models.participants import Participants
from database.models.projects import Projects

__all__ = [Projects, Participants]
db.generate_mapping(create_tables=True)
