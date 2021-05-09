import pytest
from database.repositories.participants import ParticipantsRepository
from database.repositories.projects import ProjectsRepository
from schemas.employees import EmployeeData
from schemas.projects import ProjectInterface
from services.participants import ParticipantsService
from tests.utils import generate_test_project
from utils.exceptions import AssignEmployeeException, DifferentDepartmentException, OwnerAlreadyExistsException


def test_assign_employee_to_project_already_owner(mocker):
    pj = generate_test_project()
    mock_part_repo = mocker.Mock(ParticipantsRepository)
    mock_proj_repo = mocker.Mock(ProjectsRepository)

    service = ParticipantsService(participants_repository=mock_part_repo, project_repository=mock_proj_repo)

    mock_proj_repo.check_owner.return_value = True

    employee = EmployeeData(
        id="test",
        fullname="test",
        department="test",
        is_owner=True,
    )
    project = ProjectInterface.parse_obj(pj.to_dict())

    with pytest.raises(OwnerAlreadyExistsException):
        service.assign_employee_to_project(project=project, employee=employee)


def test_assign_employee_to_project_diff_department(mocker):
    pj = generate_test_project()
    mock_part_repo = mocker.Mock(ParticipantsRepository)
    mock_proj_repo = mocker.Mock(ProjectsRepository)

    service = ParticipantsService(participants_repository=mock_part_repo, project_repository=mock_proj_repo)

    mock_proj_repo.check_owner.return_value = False
    mock_proj_repo.check_department.return_value = False

    employee = EmployeeData(
        id="test",
        fullname="test",
        department="test",
        is_owner=False,
    )
    project = ProjectInterface.parse_obj(pj.to_dict())

    with pytest.raises(DifferentDepartmentException):
        service.assign_employee_to_project(project=project, employee=employee)


def test_assign_employee_to_project_fail_to_create(mocker):
    pj = generate_test_project()
    mock_part_repo = mocker.Mock(ParticipantsRepository)
    mock_proj_repo = mocker.Mock(ProjectsRepository)

    service = ParticipantsService(participants_repository=mock_part_repo, project_repository=mock_proj_repo)

    mock_proj_repo.check_owner.return_value = False
    mock_proj_repo.check_department.return_value = True
    mock_part_repo.create.return_value = None

    employee = EmployeeData(
        id="test",
        fullname="test",
        department="test",
        is_owner=True,
    )
    project = ProjectInterface.parse_obj(pj.to_dict())

    with pytest.raises(AssignEmployeeException):
        service.assign_employee_to_project(project=project, employee=employee)


def test_assign_employee_to_project(mocker):
    pj = generate_test_project()
    mock_part_repo = mocker.Mock(ParticipantsRepository)
    mock_proj_repo = mocker.Mock(ProjectsRepository)

    service = ParticipantsService(participants_repository=mock_part_repo, project_repository=mock_proj_repo)

    mock_proj_repo.check_owner.return_value = False
    mock_proj_repo.check_department.return_value = True
    mock_part_repo.create.return_value = {"test": "test"}

    employee = EmployeeData(
        id="test",
        fullname="test",
        department="test",
        is_owner=True,
    )
    project = ProjectInterface.parse_obj(pj.to_dict())

    result = service.assign_employee_to_project(project=project, employee=employee)

    assert result == {"test": "test"}
