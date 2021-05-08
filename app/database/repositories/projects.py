from datetime import datetime
from typing import Optional

from database import Projects
from pony.orm import commit, db_session, exists, select
from schemas.projects import CreateProjectRequest, ProjectInterface, ProjectsListInterface
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

    @db_session
    def list(self) -> ProjectsListInterface:
        projects = select(poj for poj in Projects)
        if not projects:
            return ProjectsListInterface(projects=None)
        return ProjectsListInterface(projects=[ProjectInterface.parse_obj(project.to_dict()) for project in projects])

    @db_session
    def check_owner(self) -> bool:
        owner_exists = exists(proj for proj in Projects if proj.participants.filter(lambda p: p.is_owner is True))
        return owner_exists

    @db_session
    def check_department(self, department: str) -> bool:
        same_department = exists(
            proj for proj in Projects if proj.participants.filter(lambda p: p.department == department)
        )
        return same_department
