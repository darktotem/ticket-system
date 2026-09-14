import unittest

from models.manager import Manager

class TestManager(unittest.TestCase):
    def setUp(self):
        self.manager = Manager("Osteen", "osteen@gmailcom", "iopjklnm@123")

    def test_role_is_manager(self):
        self.assertEqual(self.manager.role, "manager")

    def test_view_tickets_returns_tickets(self):
        tickets = ["ticket1", "ticket2"]
        result = self.manager.view_tickets(tickets)
        self.assertEqual(result, tickets)

    def test_from_dict(self):
        data = {"name": "Osteen", "email": "osteen@gmail.com", "password_hash": "iopjklnm@123"}
        manager = Manager.from_dict(data)
        self.assertEqual(manager.name, "Osteen")
        self.assertEqual(manager.role, "manager")


if __name__ == "__main__":
    unittest.main()