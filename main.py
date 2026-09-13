class TicketApp:
    def __init__(self):
        self.auth = AuthManager()
        self.tickets = TicketManager()
        self.current_user = None
        
   #Declaring roles for someone to log in as.
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

    #Hii ni landing page for people who are not logged in yet Do not touch.
    def show_guest_menu(self):
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            self.register()
        elif choice == "2":
            self.login()
        elif choice == "3":
            print("Goodbye.")
            sys.exit(0)
        else:
            print("Invalid option.")

    def register(self):
        print("\n-- Register --")
        print("1. Customer\n2. Employee\n3. Manager")
        role_choice = input("Register as: ").strip()
        role = {"1": "user", "2": "employee", "3": "manager"}.get(role_choice)
        if not role:
            print("Invalid role choice.")
            return

        name = input("Name: ").strip()
        email = input("Email: ").strip()
        password = getpass.getpass("Password: ")

        extra = {}
        if role == "employee":
            extra["employee_id"] = input("Employee ID: ").strip()
            extra["manager_email"] = input("Manager email: ").strip()

        try:
            self.auth.register(name, email, password, role=role, **extra)
            print(f"Account created. You can now log in as a {role}.")
        except ValueError as error:
            print(f"Error: {error}")

    def login(self):
        print("\n-- Login --")
        email = input("Email: ").strip()
        password = getpass.getpass("Password: ")
        user = self.auth.login(email, password)
        if user:
            self.current_user = user
            print(f"Welcome, {user.name} ({user.role}).")
        else:
            print("Invalid email or password.")

    def logout(self):
        print(f"Goodbye, {self.current_user.name}.")
        self.current_user = None