import logging
from typing import Optional

from database import Projects
from database.repositories.projects import ProjectsRepository
from schemas.projects import CreateProjectRequest, ProjectInterface
from utils.exceptions import ProjectNotCreatedException, ProjectNotFoundException

logger = logging.getLogger(__name__)


class ProjectService:
    def __init__(
        self,
        *,
        project_repository: Optional[ProjectsRepository] = None,
    ):
        self.project_repository = project_repository or ProjectsRepository()

    def get(self, project_id: int) -> Optional[Projects]:

        project = self.project_repository.get(project_id=project_id)

        if project is None:
            logger.error(f"Project id={project_id} not found")
            raise ProjectNotFoundException

        return project

    def create(self, data: CreateProjectRequest) -> Optional[ProjectInterface]:

        created_project = self.project_repository.create(data)

        if created_project is None:
            logger.error(f"Project {data.dict()} not created")
            raise ProjectNotCreatedException

        return created_project

    def update(self, project_id: int, data: dict) -> Optional[ProjectInterface]:
        filtered = {k: v for k, v in data.items() if v is not None}
        data.clear()
        data.update(filtered)
        project = self.project_repository.update(project_id=project_id, data=data)
        return project
