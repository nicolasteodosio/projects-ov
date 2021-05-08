from datetime import datetime

from database.repositories.projects import ProjectsRepository
from freezegun import freeze_time
from pony.orm import commit, db_session
from schemas.projects import CreateProjectRequest, ProjectInterface, ProjectsListInterface
from tests.utils import generate_test_participant, generate_test_project


@db_session
def test_get_find():
    pj = generate_test_project()
    commit()

    repo = ProjectsRepository()
    result = repo.get(pj.id)
    assert result == ProjectInterface.parse_obj(pj.to_dict())


@db_session
def test_get_not_find():
    repo = ProjectsRepository()
    result = repo.get(12)
    assert result is None


@freeze_time("2021-01-01")
@db_session
def test_create():
    repo = ProjectsRepository()
    result = repo.create(CreateProjectRequest(name="other test"))
    assert result == ProjectInterface(
        id=1,
        name="other test",
        owner=None,
        participants=None,
        state="planned",
        progress=0.0,
        created_at=datetime.now(),
    )


@freeze_time("2021-01-01")
@db_session
def test_update():
    pj = generate_test_project()
    commit()
    repo = ProjectsRepository()
    result = repo.update(project_id=pj.id, data={"name": "hey"})
    assert result == ProjectInterface(
        id=1, name="hey", owner=None, participants=None, state="planned", progress=0.0, created_at=datetime.now()
    )


@freeze_time("2021-01-01")
@db_session
def test_list():
    generate_test_project()
    commit()
    repo = ProjectsRepository()
    result = repo.list()
    assert result == ProjectsListInterface(
        projects=[
            ProjectInterface(
                id=1,
                name="test",
                owner=None,
                participants=None,
                state="planned",
                progress=0.0,
                created_at=datetime.now(),
            )
        ]
    )


@freeze_time("2021-01-01")
@db_session
def test_list_none():
    repo = ProjectsRepository()
    result = repo.list()
    assert result == []


@db_session
def test_check_owner():
    pj = generate_test_project()
    generate_test_participant(project_id=pj.id)
    commit()
    repo = ProjectsRepository()
    result = repo.check_owner()
    assert result is True


@db_session
def test_check_owner_false():
    pj = generate_test_project()
    generate_test_participant(project_id=pj.id, is_owner=False)
    commit()
    repo = ProjectsRepository()
    result = repo.check_owner()
    assert result is False


@db_session
def test_check_department():
    pj = generate_test_project()
    part = generate_test_participant(project_id=pj.id)
    commit()
    repo = ProjectsRepository()
    result = repo.check_department(department=part.department)
    assert result is True


@db_session
def test_check_department_false():
    pj = generate_test_project()
    generate_test_participant(project_id=pj.id)
    commit()
    repo = ProjectsRepository()
    result = repo.check_department(department="fail")
    assert result is False
