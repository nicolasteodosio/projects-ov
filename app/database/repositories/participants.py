from datetime import datetime
from typing import Optional

from database import Participants, Projects
from pony.orm import commit, db_session, select
from schemas.employees import EmployeeData
from schemas.participants import ListParticipantInterface, ParticipantInterface
from schemas.projects import ProjectInterface


class ParticipantsRepository:
    @db_session
    def create(self, project: ProjectInterface, employee: EmployeeData) -> Optional[ParticipantInterface]:
        created_participant = Participants(
            employee_id=employee.id,
            full_name=employee.fullname,
            department=employee.department,
            is_owner=employee.is_owner,
            created_at=datetime.now(),
            project=Projects[project.id],
        )
        commit()
        return None if created_participant is None else ParticipantInterface.parse_obj(created_participant.to_dict())

    @db_session
    def get_participants(self, project_id: int) -> ListParticipantInterface:
        participants = select(pa for pa in Participants if pa.project.id == project_id)
        if not participants:
            return ListParticipantInterface(participants=None)
        return ListParticipantInterface(
            participants=[ParticipantInterface.parse_obj(participant.to_dict()) for participant in participants]
        )
