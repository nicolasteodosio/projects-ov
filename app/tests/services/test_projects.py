from datetime import datetime

import pytest
from database.repositories.participants import ParticipantsRepository
from database.repositories.projects import ProjectsRepository
from freezegun import freeze_time
from schemas.participants import ListParticipantInterface, ParticipantInterface
from schemas.projects import CreateProjectRequest, ProjectInterface, ProjectsListInterface
from services.projects import ProjectService
from tests.utils import generate_test_participant, generate_test_project
from utils.exceptions import ProjectNotCreatedException, ProjectNotFoundException


def test_get_raise_exception(mocker):
    mock_part_repo = mocker.Mock(ParticipantsRepository)
    mock_proj_repo = mocker.Mock(ProjectsRepository)

    service = ProjectService(project_repository=mock_proj_repo, participants_repository=mock_part_repo)

    mock_proj_repo.get.return_value = None
    with pytest.raises(ProjectNotFoundException):
        service.get(project_id=1)


def test_get(mocker):
    mock_part_repo = mocker.Mock(ParticipantsRepository)
    mock_proj_repo = mocker.Mock(ProjectsRepository)

    service = ProjectService(project_repository=mock_proj_repo, participants_repository=mock_part_repo)

    mock_proj_repo.get.return_value = {"ok"}
    result = service.get(project_id=1)

    assert result == {"ok"}


def test_create_raise_exception(mocker):
    mock_part_repo = mocker.Mock(ParticipantsRepository)
    mock_proj_repo = mocker.Mock(ProjectsRepository)

    service = ProjectService(project_repository=mock_proj_repo, participants_repository=mock_part_repo)

    mock_proj_repo.create.return_value = None
    with pytest.raises(ProjectNotCreatedException):
        service.create(data=CreateProjectRequest(name="test"))


def test_create(mocker):
    mock_part_repo = mocker.Mock(ParticipantsRepository)
    mock_proj_repo = mocker.Mock(ProjectsRepository)

    service = ProjectService(project_repository=mock_proj_repo, participants_repository=mock_part_repo)

    mock_proj_repo.create.return_value = {"ok"}
    result = service.create(data=CreateProjectRequest(name="test"))

    assert result == {"ok"}


def test_update(mocker):
    pj = generate_test_project()
    mock_part_repo = mocker.Mock(ParticipantsRepository)
    mock_proj_repo = mocker.Mock(ProjectsRepository)

    service = ProjectService(project_repository=mock_proj_repo, participants_repository=mock_part_repo)

    mock_proj_repo.update.return_value = {"ok"}
    result = service.update(pj.id, data={"test": "test"})

    assert result == {"ok"}
    mock_proj_repo.update.assert_called_once_with(data={"test": "test"}, project_id=1)


def test_update_cleaning_data(mocker):
    pj = generate_test_project()
    mock_part_repo = mocker.Mock(ParticipantsRepository)
    mock_proj_repo = mocker.Mock(ProjectsRepository)

    service = ProjectService(project_repository=mock_proj_repo, participants_repository=mock_part_repo)

    mock_proj_repo.update.return_value = {"ok"}
    result = service.update(pj.id, data={"test": "test", "other": None})

    assert result == {"ok"}
    mock_proj_repo.update.assert_called_once_with(data={"test": "test"}, project_id=1)


def test_list(mocker):
    mock_part_repo = mocker.Mock(ParticipantsRepository)
    mock_proj_repo = mocker.Mock(ProjectsRepository)

    service = ProjectService(project_repository=mock_proj_repo, participants_repository=mock_part_repo)

    mock_proj_repo.list.return_value = ProjectsListInterface(projects=[])
    result = service.list()

    assert result == ProjectsListInterface(projects=[])


@freeze_time("2021-01-01")
def test_list_finding(mocker):
    pj = generate_test_project()
    part = generate_test_participant(project_id=pj.id)
    mock_part_repo = mocker.Mock(ParticipantsRepository)
    mock_proj_repo = mocker.Mock(ProjectsRepository)

    service = ProjectService(project_repository=mock_proj_repo, participants_repository=mock_part_repo)

    mock_proj_repo.list.return_value = ProjectsListInterface(projects=[ProjectInterface.parse_obj(pj.to_dict())])
    mock_part_repo.get_participants.return_value = ListParticipantInterface(
        participants=[ParticipantInterface.parse_obj(part.to_dict())]
    )
    result = service.list()

    assert result == ProjectsListInterface(
        projects=[
            ProjectInterface(
                id=1,
                name="test",
                owner=ParticipantInterface(
                    id=1,
                    employee_id="test",
                    full_name="test",
                    department="test",
                    is_owner=True,
                    created_at=datetime.now(),
                ),
                participants=[],
                state="planned",
                progress=0.0,
                created_at=datetime.now(),
            )
        ]
    )


@freeze_time("2021-01-01")
def test_list_finding_multiples(mocker):
    pj = generate_test_project()
    part = generate_test_participant(project_id=pj.id)
    part2 = generate_test_participant(project_id=pj.id, is_owner=False, id=2)
    mock_part_repo = mocker.Mock(ParticipantsRepository)
    mock_proj_repo = mocker.Mock(ProjectsRepository)

    service = ProjectService(project_repository=mock_proj_repo, participants_repository=mock_part_repo)

    mock_proj_repo.list.return_value = ProjectsListInterface(projects=[ProjectInterface.parse_obj(pj.to_dict())])
    mock_part_repo.get_participants.return_value = ListParticipantInterface(
        participants=[
            ParticipantInterface.parse_obj(part.to_dict()),
            ParticipantInterface.parse_obj(part2.to_dict()),
        ]
    )
    result = service.list()

    assert result == ProjectsListInterface(
        projects=[
            ProjectInterface(
                id=1,
                name="test",
                owner=ParticipantInterface(
                    id=1,
                    employee_id="test",
                    full_name="test",
                    department="test",
                    is_owner=True,
                    created_at=datetime.now(),
                ),
                participants=[
                    ParticipantInterface(
                        id=2,
                        employee_id="test",
                        full_name="test",
                        department="test",
                        is_owner=False,
                        created_at=datetime.now(),
                    )
                ],
                state="planned",
                progress=0.0,
                created_at=datetime.now(),
            )
        ]
    )
