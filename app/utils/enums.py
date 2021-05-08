from enum import Enum


class ProjectStatus(Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    DONE = "done"
    FAILED = "failed"
