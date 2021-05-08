from datetime import datetime

from database import Participants, Projects
from pony.orm import db_session
from utils.enums import ProjectStatus


@db_session
def generate_test_project(**kwargs):
    fields = {
        "id": 1,
        "name": "test",
        "state": ProjectStatus.PLANNED.value,
        "progress": 0.0,
        "created_at": datetime.now(),
    }
    fields.update(**kwargs)
    return Projects(**fields)


@db_session
def generate_test_participant(project_id, **kwargs):
    fields = {
        "id": 1,
        "project": project_id,
        "is_owner": True,
        "department": "test",
        "full_name": "test",
        "employee_id": "test",
        "created_at": datetime.now(),
    }
    fields.update(**kwargs)
    return Participants(**fields)
