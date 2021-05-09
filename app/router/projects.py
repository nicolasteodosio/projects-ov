import logging

from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from schemas.projects import (
    AssignParticipantRequest,
    CreateProjectRequest,
    ProjectInterface,
    ProjectsListInterface,
    UpdateProjectRequest,
)
from services.employees import EmployeesService
from services.participants import ParticipantsService
from services.projects import ProjectService
from starlette import status
from starlette.responses import JSONResponse
from utils.exceptions import (
    AssignEmployeeException,
    DifferentDepartmentException,
    EmployeesApiException,
    EmployeesNotFoundException,
    OwnerAlreadyExistsException,
    ProjectNotCreatedException,
    ProjectNotFoundException,
)

router = InferringRouter()
logger = logging.Logger(__name__)


@cbv(router)
class ProjectView:
    def __init__(self, *, projects_service=None, participants_service=None, employees_service=None):
        self.projects_service = projects_service or ProjectService()
        self.employees_service = employees_service or EmployeesService()
        self.participants_service = participants_service or ParticipantsService()

    @router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ProjectInterface)
    def create(self, data: CreateProjectRequest):
        try:
            created_project = self.projects_service.create(data)
            if created_project:
                return JSONResponse(content=jsonable_encoder(created_project), status_code=status.HTTP_201_CREATED)

        except ProjectNotCreatedException as ex:
            logger.error(f"Unknown error, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": f"Could not create project ex: {ex}"},
            )
        except Exception as ex:
            logger.error(f"Unknown error, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": f"An unknown error occurred ex: {ex}"},
            )

    @router.get("/list", status_code=status.HTTP_200_OK, response_model=ProjectsListInterface)
    def list(self):
        try:
            projects = self.projects_service.list()
            return JSONResponse(content=jsonable_encoder(projects), status_code=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(f"Unknown error, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": f"An unknown error occurred ex: {ex}"},
            )

    @router.put("/{project_id}", status_code=status.HTTP_202_ACCEPTED)
    def update(self, project_id: int, data: UpdateProjectRequest):
        try:
            project = self.projects_service.get(project_id)
            updated_project = self.projects_service.update(project.id, data.dict())
            if updated_project:
                return JSONResponse(content=jsonable_encoder(updated_project), status_code=status.HTTP_202_ACCEPTED)

        except ProjectNotFoundException as ex:
            logger.error(f"Project not found, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"title": "Error", "message": f"Project id={project_id} not found"},
            )

        except Exception as ex:
            logger.error(f"Unknown error, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": f"An unknown error occurred ex: {ex}"},
            )

    @router.post(
        "/assign/{project_id}",
        status_code=status.HTTP_201_CREATED,
    )
    def assign(self, project_id: int, data: AssignParticipantRequest):
        try:
            project = self.projects_service.get(project_id)
            employee = self.employees_service.get(is_owner=data.is_owner, department=data.department)
            participant_to_project = self.participants_service.assign_employee_to_project(
                project=project, employee=employee
            )

            if participant_to_project:
                return JSONResponse(
                    content={
                        "title": "Success",
                        "message": f"An employee was assigned to the project id: {project_id}",
                    },
                    status_code=status.HTTP_201_CREATED,
                )

        except ProjectNotFoundException as ex:
            logger.error(f"Project not found, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"title": "Error", "message": f"Project id={project_id} not found"},
            )

        except EmployeesApiException as ex:
            logger.error(f"Employees Api error, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": "Employees Api error"},
            )
        except EmployeesNotFoundException as ex:
            logger.error(f"Employees not found with the parameters, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": "Employees not found with the parameters"},
            )

        except OwnerAlreadyExistsException as ex:
            logger.error(f"Project already has an owner, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": "Project already has an owner"},
            )

        except DifferentDepartmentException as ex:
            logger.error(f"Project has different department, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": "Project has different department"},
            )

        except AssignEmployeeException as ex:
            logger.error(f"Error when assign employee, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": "Error when assign employee"},
            )

        except Exception as ex:
            logger.error(f"Unknown error, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": f"An unknown error occurred ex: {ex}"},
            )
