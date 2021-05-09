from datetime import datetime

from database.repositories.participants import ParticipantsRepository
from freezegun import freeze_time
from pony.orm import commit, db_session
from schemas.employees import EmployeeData
from schemas.participants import ListParticipantInterface, ParticipantInterface
from schemas.projects import ProjectInterface
from tests.utils import generate_test_participant, generate_test_project


@freeze_time("2021-01-01")
@db_session
def test_create():
    pj = generate_test_project()

    repo = ParticipantsRepository()
    result = repo.create(
        ProjectInterface.parse_obj(pj.to_dict()),
        EmployeeData(id="test", fullname="test", is_owner=True, department="test"),
    )

    assert result == ParticipantInterface(
        id=1, employee_id="test", full_name="test", department="test", is_owner=True, created_at=datetime.now()
    )


@freeze_time("2021-01-01")
@db_session
def test_get_participants():
    pj = generate_test_project()
    generate_test_participant(project_id=pj.id)
    commit()

    repo = ParticipantsRepository()
    result = repo.get_participants(project_id=pj.id)

    assert result == ListParticipantInterface(
        participants=[
            ParticipantInterface(
                id=1, employee_id="test", full_name="test", department="test", is_owner=True, created_at=datetime.now()
            )
        ]
    )


@freeze_time("2021-01-01")
@db_session
def test_get_participants_empty():
    pj = generate_test_project()
    commit()

    repo = ParticipantsRepository()
    result = repo.get_participants(project_id=pj.id)

    assert result == ListParticipantInterface(participants=None)
