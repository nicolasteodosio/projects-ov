from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from schemas.participants import ParticipantInterface


class CreateProjectRequest(BaseModel):
    name: str


class UpdateProjectRequest(BaseModel):
    name: Optional[str]
    state: Optional[str]
    progress: Optional[float]


class ProjectInterface(BaseModel):
    id: int
    name: str
    owner: Optional[ParticipantInterface]
    participants: Optional[List[ParticipantInterface]]
    state: str
    progress: float
    created_at: datetime


class AssignParticipantRequest(BaseModel):
    department: str
    is_owner: bool


class ProjectsListInterface(BaseModel):
    projects: Optional[List[ProjectInterface]]
