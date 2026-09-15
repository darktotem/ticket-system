from models.manager import Manager
from models.user import User


def test_manager_role_is_manager():
    manager = Manager("Osteen", "osteen@gmail.com", "somehash")
    assert manager.role == "manager"


def test_manager_inherits_password_check():
    manager = Manager("Osteen", "osteen@gmail.com", User.hash_password("pass1234"))
    assert manager.check_password("pass1234") is True
    assert manager.check_password("wrong") is False


def test_manager_to_dict_has_no_employee_only_fields():
    manager = Manager("Osteen", "osteen@gmail.com", "somehash")
    data = manager.to_dict()
    assert data == {
        "name": "Osteen",
        "email": "osteen@gmail.com",
        "password_hash": "somehash",
        "role": "manager",
    }
    assert "employee_id" not in data


def test_from_dict_roundtrip():
    original = Manager("Osteen", "osteen@gmail.com", User.hash_password("pass1234"))
    rebuilt = Manager.from_dict(original.to_dict())

    assert rebuilt.name == original.name
    assert rebuilt.email == original.email
    assert rebuilt.check_password("pass1234") is True
    assert rebuilt.role == "manager"