from pathlib import Path

from models.employee import Employee
from models.manager import Manager
from models.user import User
from utils.storage import load_json, save_json
from utils.validators import not_empty, valid_email

ROLE_CLASSES = {
    "user": User,
    "employee": Employee,
    "manager": Manager,
}


class AuthManager:
    def __init__(self, users_file="data/users.json"):
        self.users_file = Path(users_file)

    def register(self, name, email, password, role="user", **extra):
        name = name.strip()
        email = email.strip().lower()
        role = role.strip().lower()

        if not not_empty(name):
            raise ValueError("Name cannot be empty.")
        if not valid_email(email):
            raise ValueError("Please enter a valid email.")
        if len(password) < 4:
            raise ValueError("Password must have at least 4 characters.")
        if role not in ROLE_CLASSES:
            raise ValueError("Role must be one of: user, employee, manager.")

        users = load_json(self.users_file)

        for saved_user in users:
            if saved_user["email"].lower() == email:
                raise ValueError("An account with that email already exists.")

        password_hash = User.hash_password(password)
        user_class = ROLE_CLASSES[role]

        if role == "employee":
            user = user_class(
                name,
                email,
                password_hash,
                employee_id=extra.get("employee_id"),
                manager_email=extra.get("manager_email"),
            )
        else:
            user = user_class(name, email, password_hash)

        users.append(user.to_dict())
        save_json(self.users_file, users)
        return user

    def login(self, email, password):
        email = email.strip().lower()
        users = load_json(self.users_file)

        for saved_user in users:
            if saved_user["email"].lower() == email:
                user_class = ROLE_CLASSES.get(saved_user["role"], User)
                user = user_class.from_dict(saved_user)

                if user.check_password(password):
                    return user
                return None

        return None

    def find_by_email(self, email):
        email = email.strip().lower()
        users = load_json(self.users_file)
        for saved_user in users:
            if saved_user["email"].lower() == email:
                user_class = ROLE_CLASSES.get(saved_user["role"], User)
                return user_class.from_dict(saved_user)
        return None

    def list_employees(self):
        users = load_json(self.users_file)
        return [Employee.from_dict(u) for u in users if u.get("role") == "employee"]
