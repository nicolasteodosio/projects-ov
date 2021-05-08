from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CreateProjectRequest(BaseModel):
    name: str


class UpdateProjectRequest(BaseModel):
    name: Optional[str]
    state: Optional[str]
    progress: Optional[float]


class ProjectInterface(BaseModel):
    id: int
    name: str
    owner: Optional[int]
    participants: Optional[int]
    state: str
    progress: float
    created_at: datetime


class AssignParticipantRequest(BaseModel):
    department: str
    is_owner: bool


class ProjectsListInterface(BaseModel):
    projects: List[ProjectInterface]
