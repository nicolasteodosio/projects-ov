import pytest
from config import EMPLOYEES_API
from services.employees import EmployeesService
from utils.exceptions import EmployeesApiException, EmployeesNotFoundException


def test_get_not_200(requests_mock):
    requests_mock.get(f"{EMPLOYEES_API}", status_code=500)
    service = EmployeesService()
    with pytest.raises(EmployeesApiException):
        service.get(is_owner=True, department="test")


def test_get_employee_not_found(requests_mock):
    requests_mock.get(
        f"{EMPLOYEES_API}",
        status_code=200,
        json={
            "data": [
                {
                    "id": "d6c7ad7e-a8a9-4747-9de6-32d7567a969c",
                    "first_name": "Carmencita",
                    "last_name": "Southcomb",
                    "email": "carmencita.southcomb@acme.com",
                    "department": "engineering",
                    "role": "employee",
                },
            ]
        },
    )
    service = EmployeesService()
    with pytest.raises(EmployeesApiException):
        service.get(is_owner=True, department="test")


def test_get(requests_mock):
    requests_mock.get(
        f"{EMPLOYEES_API}",
        status_code=200,
        json={
            "data": [
                {
                    "id": "d6c7ad7e-a8a9-4747-9de6-32d7567a969c",
                    "first_name": "Carmencita",
                    "last_name": "Southcomb",
                    "email": "carmencita.southcomb@acme.com",
                    "department": "engineering",
                    "role": "employee",
                },
            ]
        },
    )
    service = EmployeesService()
    with pytest.raises(EmployeesNotFoundException):
        service.get(is_owner=False, department="sales")
