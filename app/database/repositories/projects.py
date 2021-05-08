from datetime import datetime
from typing import Optional

from database import Projects
from pony.orm import commit, db_session, select
from schemas.projects import CreateProjectRequest, ProjectInterface
from utils.enums import ProjectStatus


class ProjectsRepository:
    @db_session
    def get(self, project_id: int) -> Optional[ProjectInterface]:
        project = select(proj for proj in Projects if proj.id == project_id).first()
        if project:
            return ProjectInterface.parse_obj(project.to_dict())
        return None

    @db_session
    def create(self, data: CreateProjectRequest) -> Optional[ProjectInterface]:
        created_project = Projects(
            name=data.name,
            state=ProjectStatus.PLANNED.value,
            progress=0.0,
            created_at=datetime.now(),
        )
        commit()
        return None if created_project is None else ProjectInterface.parse_obj(created_project.to_dict())

    @db_session
    def update(self, project_id: int, data: dict) -> ProjectInterface:
        project = select(proj for proj in Projects if proj.id == project_id).first()
        project.set(**data)
        return ProjectInterface.parse_obj(project.to_dict())
