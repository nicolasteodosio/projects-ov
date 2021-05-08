from pydantic import BaseModel


class EmployeeData(BaseModel):
    id: str
    fullname: str
    department: str
    is_owner: bool
