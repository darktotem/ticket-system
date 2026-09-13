from models.user import User

class Employee(User):
    

    role = "employee"

    def __init__(self, name, email, password_hash):
        super().__init__(name, email, password_hash)
        self.role = "employee"