from models.user import User


class Employee(User):
    """Customer care agent who works tickets."""

    role = "employee"

    def __init__(self, name, email, password_hash, employee_id=None, manager_email=None):
        super().__init__(name, email, password_hash)
        self.employee_id = employee_id
        self.manager_email = manager_email

    def to_dict(self):
        data = super().to_dict()
        data["employee_id"] = self.employee_id
        data["manager_email"] = self.manager_email
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["email"],
            data["password_hash"],
            data.get("employee_id"),
            data.get("manager_email"),
        )
