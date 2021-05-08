from database.repositories.participants import ParticipantsRepository
from schemas.employees import EmployeeData
from schemas.projects import ProjectInterface


class ParticipantsService:
    def __init__(self, *, participants_repository=None):
        self.repository = participants_repository or ParticipantsRepository()

    def assign_employee_to_project(self, project: ProjectInterface, employee: EmployeeData):
        assigned_employee = self.repository.create(project, employee)
        if assigned_employee is None:
            raise Exception
        return assigned_employee
