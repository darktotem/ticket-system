import getpass
import sys

from utils.auth import AuthManager
from utils.decorators import employee_required, login_required, manager_required
from utils.ticket_manager import TicketManager

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

    @login_required
    def show_user_menu(self):
        print(
        "\n1. Raise a new ticket\n2. Check my ticket\n"
        "3. Respond to a proposed resolution\n4. Logout"
        )
        choice = input("Choose an option: ").strip()
        if choice == "1":
            self.raise_ticket()
        elif choice == "2":
            self.check_ticket()
        elif choice == "3":
            self.respond_to_resolution()
        elif choice == "4":
            self.logout()
        else:
            print("Invalid option.")

    @login_required
    def raise_ticket(self):
        description = input("Describe your issue: ").strip()
        ticket = self.tickets.create_ticket(self.current_user, description)
        print(f"Ticket created. Your ticket number is: {ticket.ticket_number}")

    @login_required
    def check_ticket(self):
        ticket_number = input("Enter your ticket number: ").strip()
        ticket = self.tickets.get_ticket(ticket_number)
        if not ticket or ticket.user_email != self.current_user.email:
            print("Ticket not found.")
            return
        self.print_ticket_summary(ticket)

    @login_required
    def respond_to_resolution(self):
        ticket_number = input("Enter your ticket number: ").strip()
        ticket = self.tickets.get_ticket(ticket_number)
        if not ticket or ticket.user_email != self.current_user.email:
            print("Ticket not found.")
            return

    if not ticket.resolution_summary:
        print("No resolution has been proposed for this ticket yet.")
        return

    print(f"Proposed resolution: {ticket.resolution_summary}")
    answer = input("Was your issue solved? (yes/no): ").strip().lower() 

    if answer in ("yes", "y", "solved"):
        self.tickets.confirm_resolution(ticket_number, self.current_user.email, True)
        print("Great — ticket closed.")
    else:
        feedback = input("What wasn't solved / what happened? ").strip()
        self.tickets.confirm_resolution(
            ticket_number, self.current_user.email, False, feedback
        )
        print("Got it — the ticket stays open and your note has been saved for the team.")
