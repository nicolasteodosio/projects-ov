import os
from typing import Optional

import requests
from schemas.employees import EmployeeData
from starlette import status
from utils.exceptions import EmployeesApiException, EmployeesNotFoundException


class EmployeesService:
    def __init__(self):
        self.url = os.getenv("EMPLOYEES_API")

    def get(self, is_owner: bool, department: str) -> Optional[EmployeeData]:
        response = requests.get(self.url)
        if response.status_code != status.HTTP_200_OK:
            raise EmployeesApiException

        data = response.json()
        items = data["data"]
        role = "manager" if is_owner else "employee"
        employee = next((item for item in items if item["role"] == role and item["department"] == department), None)
        if employee is None:
            raise EmployeesNotFoundException

        emp_data = EmployeeData(
            id=employee["id"],
            fullname=f"{employee['first_name']} {employee['last_name']}",
            department=employee["department"],
            is_owner=is_owner,
        )
        return emp_data
