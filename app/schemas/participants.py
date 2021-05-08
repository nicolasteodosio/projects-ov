from datetime import datetime

from pydantic import BaseModel


class ParticipantInterface(BaseModel):
    id: int
    employee_id: str
    full_name: str
    department: str
    is_owner: bool
    created_at: datetime
