import hashlib


class User:
    """The customer or inquirer who raises tickets."""

    role = "user"

    def __init__(self, name, email, password_hash):
        self.name = name
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def check_password(self, password):
        return self.password_hash == self.hash_password(password)

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role,
        }

class Manager(User):
    def __init__(self, name, email, password_hash):
        super().__init__(name, email, password_hash)
        self.role = "manager"
