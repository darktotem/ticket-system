from models.employee import Employee
from models.user import User


def test_employee_role_is_employee():
    """Test that the role attribute of an Employee instance is 'employee'."""
    employee = Employee("Faith Ndiritu", "faith@example.com", "somehash")
    assert employee.role == "employee"


def test_employee_inherits_password_check():
    """Test that the Employee class inherits the password checking functionality from User."""
    employee = Employee("Faith Ndiritu", "faith@example.com", User.hash_password("pass1234"))
    assert employee.check_password("pass1234") is True
    assert employee.check_password("wrong") is False


def test_employee_stores_employee_id_and_manager_email():
    """Test that the Employee class correctly stores employee_id and manager_email."""
    employee = Employee(
        "Faith Ndiritu", "faith@example.com", "somehash", employee_id="E001", manager_email="mgr@example.com"
    )
    assert employee.employee_id == "E001"
    assert employee.manager_email == "mgr@example.com"


def test_employee_id_and_manager_email_default_to_none():
    """Test that employee_id and manager_email default to None if not provided."""
    employee = Employee("Faith Ndiritu", "faith@example.com", "somehash")
    assert employee.employee_id is None
    assert employee.manager_email is None


def test_to_dict_includes_employee_fields():
    """Test that the to_dict method includes employee_id and manager_email."""
    employee = Employee(
        "Faith Ndiritu", "faith@example.com", "somehash", employee_id="E001", manager_email="mgr@example.com"
    )
    data = employee.to_dict()
    assert data == {
        "name": "Faith Ndiritu",
        "email": "faith@example.com",
        "password_hash": "somehash",
        "role": "employee",
        "employee_id": "E001",
        "manager_email": "mgr@example.com",
    }


def test_from_dict_roundtrip():
    """Test that an Employee can be serialized to a dict and then reconstructed from that dict."""
    original = Employee(
        "Faith Ndiritu",
        "faith@example.com",
        User.hash_password("pass1234"),
        employee_id="E001",
        manager_email="mgr@example.com",
    )
    rebuilt = Employee.from_dict(original.to_dict())

    assert rebuilt.employee_id == "E001"
    assert rebuilt.manager_email == "mgr@example.com"
    assert rebuilt.check_password("pass1234") is True