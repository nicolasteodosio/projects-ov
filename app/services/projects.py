import logging
from typing import Optional, Union

from database.repositories.participants import ParticipantsRepository
from database.repositories.projects import ProjectsRepository
from schemas.projects import CreateProjectRequest, ProjectInterface, ProjectsListInterface
from utils.exceptions import ProjectNotCreatedException, ProjectNotFoundException

logger = logging.getLogger(__name__)


class ProjectService:
    def __init__(
        self,
        *,
        project_repository: Optional[ProjectsRepository] = None,
        participants_repository: Optional[ParticipantsRepository] = None,
    ):
        self.project_repository = project_repository or ProjectsRepository()
        self.participants_repository = participants_repository or ParticipantsRepository()

    def get(self, project_id: int) -> Optional[ProjectInterface]:

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

    def list(self) -> Union[list, ProjectsListInterface]:
        projects = self.project_repository.list()
        for project in projects.projects:
            participants = self.participants_repository.get_participants(project_id=project.id)
            if participants:
                find_owner = list(filter(lambda p: p.is_owner is True, participants.participants))
                project.owner = find_owner[0] if find_owner else None
                project.participants = list(filter(lambda p: p.is_owner is False, participants.participants))
        return projects
