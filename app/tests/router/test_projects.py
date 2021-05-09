from router.projects import ProjectView
from schemas.projects import AssignParticipantRequest, CreateProjectRequest, UpdateProjectRequest
from services.employees import EmployeesService
from services.participants import ParticipantsService
from services.projects import ProjectService
from utils.exceptions import (
    AssignEmployeeException,
    DifferentDepartmentException,
    EmployeesApiException,
    EmployeesNotFoundException,
    OwnerAlreadyExistsException,
    ProjectNotCreatedException,
    ProjectNotFoundException,
)


def test_create(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_proj_service.create.return_value = {"ok"}

    data = CreateProjectRequest(name="test")

    result = view.create(data)

    assert result.status_code == 201


def test_create_create_exception(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_proj_service.create.side_effect = ProjectNotCreatedException

    data = CreateProjectRequest(name="test")

    result = view.create(data)

    assert result.status_code == 500


def test_create_create_unknown_exception(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_proj_service.create.side_effect = Exception

    data = CreateProjectRequest(name="test")

    result = view.create(data)

    assert result.status_code == 500


def test_list(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_proj_service.list.return_value = []
    result = view.list()

    assert result.status_code == 200


def test_list_exception(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_proj_service.list.side_effect = Exception
    result = view.list()

    assert result.status_code == 500


def test_update(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_proj_service.update.return_value = {"ok"}
    result = view.update(project_id=1, data=UpdateProjectRequest(name="test"))

    assert result.status_code == 202


def test_update_not_found_exception(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_proj_service.get.return_value = ProjectNotFoundException
    result = view.update(project_id=1, data=UpdateProjectRequest(name="test"))

    assert result.status_code == 500


def test_update_unknow_exception(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_proj_service.get.return_value = Exception
    result = view.update(project_id=1, data=UpdateProjectRequest(name="test"))

    assert result.status_code == 500


def test_assign(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_par_service.assign_employee_to_project.return_value = {"ok"}
    result = view.assign(project_id=1, data=AssignParticipantRequest(is_owner=True, department="test"))

    assert result.status_code == 201


def test_assign_project_not_found(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_proj_service.get.side_effect = ProjectNotFoundException
    result = view.assign(project_id=1, data=AssignParticipantRequest(is_owner=True, department="test"))

    assert result.status_code == 404


def test_assign_employee_api_exception(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_emp_service.get.side_effect = EmployeesApiException
    result = view.assign(project_id=1, data=AssignParticipantRequest(is_owner=True, department="test"))

    assert result.status_code == 500


def test_assign_employee_not_found(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_emp_service.get.side_effect = EmployeesNotFoundException
    result = view.assign(project_id=1, data=AssignParticipantRequest(is_owner=True, department="test"))

    assert result.status_code == 500


def test_assign_already_has_owner(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_par_service.assign_employee_to_project.side_effect = OwnerAlreadyExistsException
    result = view.assign(project_id=1, data=AssignParticipantRequest(is_owner=True, department="test"))

    assert result.status_code == 500


def test_assign_diff_department(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_par_service.assign_employee_to_project.side_effect = DifferentDepartmentException
    result = view.assign(project_id=1, data=AssignParticipantRequest(is_owner=True, department="test"))

    assert result.status_code == 500


def test_assign_exception(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_par_service.assign_employee_to_project.side_effect = AssignEmployeeException
    result = view.assign(project_id=1, data=AssignParticipantRequest(is_owner=True, department="test"))

    assert result.status_code == 500


def test_assign_unknown_exception(mocker):
    mock_proj_service = mocker.Mock(ProjectService)
    mock_par_service = mocker.Mock(ParticipantsService)
    mock_emp_service = mocker.Mock(EmployeesService)

    view = ProjectView(
        projects_service=mock_proj_service, participants_service=mock_par_service, employees_service=mock_emp_service
    )

    mock_par_service.assign_employee_to_project.side_effect = Exception
    result = view.assign(project_id=1, data=AssignParticipantRequest(is_owner=True, department="test"))

    assert result.status_code == 500
