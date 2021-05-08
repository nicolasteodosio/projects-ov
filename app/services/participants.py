from database.repositories.participants import ParticipantsRepository
from database.repositories.projects import ProjectsRepository
from schemas.employees import EmployeeData
from schemas.projects import ProjectInterface
from utils.exceptions import AssignEmployeeException, DifferentDepartmentException, OwnerAlreadyExistsException


class ParticipantsService:
    def __init__(self, *, participants_repository=None, project_repository=None):
        self.repository = participants_repository or ParticipantsRepository()
        self.project_repository = project_repository or ProjectsRepository()

    def assign_employee_to_project(self, project: ProjectInterface, employee: EmployeeData):
        if employee.is_owner:
            exists = self.project_repository.check_owner()
            if exists:
                raise OwnerAlreadyExistsException

        match_department = self.project_repository.check_department(employee.department)
        if match_department:

            assigned_employee = self.repository.create(project, employee)
            if assigned_employee is None:
                raise AssignEmployeeException

            return assigned_employee

        raise DifferentDepartmentException
