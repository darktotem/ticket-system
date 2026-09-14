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

    #Hii ni landing page for people who are not logged in yet Do not touch (guests).
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

      #Ticket system ya Customer. (Done by Kelvin)
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

 #manager menu (Done by Kelvin)
    @manager_required
    def view_all_tickets(self):
        tickets = self.tickets.list_tickets()
        if not tickets:
            print("No tickets yet.")
        for ticket in tickets:
            print(
                f"{ticket.ticket_number} | {ticket.status} | "
                f"assigned: {ticket.assigned_employee or '-'} | {ticket.user_email}"
            )

    @manager_required
    def view_employees(self):
        employees = self.auth.list_employees()
        if not employees:
            print("No employees registered.")
        for employee in employees:
            print(f"{employee.name} | {employee.email} | ID: {employee.employee_id}")

    # Employee menu (Done by Faith.N)   

    @employee_required
    def show_employee_menu(self):
        print(
            "\n1. View open/pending tickets\n2. Open a ticket by number\n"
            "3. Log an update (mark pending)\n4. Propose a resolution\n5. Logout"
        )
        choice = input("Choose an option: ").strip()
        if choice == "1":
            self.list_open_tickets()
        elif choice == "2":
            self.view_ticket_by_number()
        elif choice == "3":
            self.update_ticket()
        elif choice == "4":
            self.propose_resolution()
        elif choice == "5":
            self.logout()
        else:
            print("Invalid option.")

    @employee_required
    def list_open_tickets(self):
        """List all tickets still needing attention ."""
        tickets = self.tickets.list_tickets(statuses=("open", "pending"))
        if not tickets:
            print("No open or pending tickets.")
        for ticket in tickets:
            print(
                f"{ticket.ticket_number} | {ticket.status} | "
                f"{ticket.user_email} | {ticket.description[:40]}"
            )

    @employee_required
    def view_ticket_by_number(self):
        """Displays full details of one ticket, including its history."""
        ticket_number = input("Ticket number: ").strip()
        ticket = self.tickets.get_ticket(ticket_number)
        if not ticket:
            print("Ticket not found.")
            return
        self.print_ticket_summary(ticket, show_history=True)

    @employee_required
    def update_ticket(self):
        """Updates the status of a ticket."""
        ticket_number = input("Ticket number: ").strip()
        action = input("What action are you taking / why is it pending? ").strip()
        ticket = self.tickets.update_ticket(ticket_number, self.current_user, action)
        if not ticket:
            print("Ticket not found.")
            return
        print(f"Ticket {ticket.ticket_number} marked as pending with your note saved.")

    @employee_required
    def propose_resolution(self):
        """Proposes a resolution for a ticket."""
        ticket_number = input("Ticket number: ").strip()
        summary = input("How was the issue resolved? ").strip()
        ticket = self.tickets.propose_resolution(ticket_number, self.current_user, summary)
        if not ticket:
            print("Ticket not found.")
            return
        print("Resolution recorded. Waiting on customer confirmation to close.")

# Ticket system (Done by victor)
# Shared helper (to view latest status of a ticket)
    def print_ticket_summary(self, ticket, show_history=False):
        print(f"\nTicket: {ticket.ticket_number}")
        print(f"Status: {ticket.status}")
        print(f"Description: {ticket.description}")
        print(f"Assigned to: {ticket.assigned_employee or 'Unassigned'}")
        if ticket.resolution_summary:
            print(f"Proposed resolution: {ticket.resolution_summary}")
        if ticket.user_feedback:
            print(f"Customer feedback: {ticket.user_feedback}")
        if show_history and ticket.history:
            print("History:")
            for entry in ticket.history:
                print(
                    f"  [{entry['timestamp']}] {entry['by']}: "
                    f"{entry['action']} (status -> {entry['status']})"
                )


if __name__ == "__main__":
    app = TicketApp()
    try:
        app.run()
    except KeyboardInterrupt: #just incase someone presses ctrl+c to exit the program.
        print("\nExiting.")

