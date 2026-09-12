from models.user import User

class Manager(User):
    """Oversees employees and has full visibility into all tickets."""

    role = "manager"

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["email"], data["password_hash"])