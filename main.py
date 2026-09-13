class TicketApp:
    def __init__(self):
        self.auth = AuthManager()
        self.tickets = TicketManager()
        self.current_user = None

    def run(self):
        print("Customer Care Ticket System")
        while True:
            if self.current_user is None:
                self.show_guest_menu()
            elif self.current_user.role == "user":
                self.show_user_menu()
            elif self.current_user.role == "employee":
                self.show_employee_menu()
            elif self.current_user.role == "manager":
                self.show_manager_menu()