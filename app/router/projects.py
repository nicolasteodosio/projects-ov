import logging

from fastapi.encoders import jsonable_encoder
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from schemas.projects import AssignParticipantRequest, CreateProjectRequest, UpdateProjectRequest
from services.employees import EmployeesService
from services.participants import ParticipantsService
from services.projects import ProjectService
from starlette import status
from starlette.responses import JSONResponse
from utils.exceptions import ProjectNotFoundException

router = InferringRouter()
logger = logging.Logger(__name__)


@cbv(router)
class ProjectView:
    def __init__(self, *, projects_service=None, participants_service=None, employees_service=None):
        self.projects_service = projects_service or ProjectService()
        self.employees_service = employees_service or EmployeesService()
        self.participants_service = participants_service or ParticipantsService()

    @router.post("/create", status_code=status.HTTP_201_CREATED)
    def create(self, data: CreateProjectRequest):
        try:
            created_project = self.projects_service.create(data)
            if created_project:
                return JSONResponse(content=jsonable_encoder(created_project), status_code=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.error(f"Unknown error, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": f"An unknown error occurred ex: {ex}"},
            )

    @router.get("/list", status_code=status.HTTP_200_OK)
    def list(self, data: CreateProjectRequest):
        pass

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

    @router.post("/assign/{project_id}", status_code=status.HTTP_201_CREATED)
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
        except Exception as ex:
            logger.error(f"Unknown error, ex: {ex}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"title": "Error", "message": f"An unknown error occurred ex: {ex}"},
            )
