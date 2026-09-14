from datetime import datetime
from pathlib import Path

from models.ticket import Ticket
from utils.storage import load_json, save_json


class TicketManager:
    def __init__(self, tickets_file="data/tickets.json"):
        self.tickets_file = Path(tickets_file)

    def _load(self):
        return [Ticket.from_dict(t) for t in load_json(self.tickets_file)]

    def _save(self, tickets):
        save_json(self.tickets_file, [t.to_dict() for t in tickets])

    def _log(self, ticket, by, action, status):
        ticket.history.append(
            {
                "by": by,
                "action": action,
                "status": status,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            }
        )

    def create_ticket(self, user, description):
        ticket = Ticket(
            user_name=user.name,
            user_email=user.email,
            description=description,
            status="open",
        )
        self._log(ticket, user.email, f"Raised ticket: {description}", "open")
        tickets = self._load()
        tickets.append(ticket)
        self._save(tickets)
        return ticket

    def get_ticket(self, ticket_number):
        for ticket in self._load():
            if ticket.ticket_number == ticket_number:
                return ticket
        return None

    def list_tickets(self, statuses=None):
        tickets = self._load()
        if statuses:
            tickets = [t for t in tickets if t.status in statuses]
        return tickets

    def _update_and_save(self, ticket_number, mutate_fn):
        tickets = self._load()
        for index, ticket in enumerate(tickets):
            if ticket.ticket_number == ticket_number:
                mutate_fn(ticket)
                ticket.touch()
                tickets[index] = ticket
                self._save(tickets)
                return ticket
        return None

    def update_ticket(self, ticket_number, employee, action_taken):
        """Employee logs progress / why it's still pending."""

        def mutate(ticket):
            ticket.assigned_employee = employee.email
            ticket.action_taken = action_taken
            ticket.status = "pending"
            self._log(ticket, employee.email, action_taken, "pending")

        return self._update_and_save(ticket_number, mutate)

    def propose_resolution(self, ticket_number, employee, resolution_summary):
        """Employee believes the issue is fixed; awaiting customer confirmation."""

        def mutate(ticket):
            ticket.assigned_employee = employee.email
            ticket.resolution_summary = resolution_summary
            ticket.status = "pending"
            self._log(
                ticket,
                employee.email,
                f"Proposed resolution: {resolution_summary}",
                "pending",
            )

        return self._update_and_save(ticket_number, mutate)

    def confirm_resolution(self, ticket_number, user_email, agreed, feedback=""):
        """Customer confirms whether the proposed resolution actually solved it."""

        def mutate(ticket):
            ticket.user_agreed_to_close = agreed
            if agreed:
                ticket.status = "closed"
                ticket.user_feedback = ""
                self._log(ticket, user_email, "Confirmed resolution", "closed")
            else:
                ticket.status = "pending"
                ticket.user_feedback = feedback
                self._log(
                    ticket,
                    user_email,
                    f"Rejected resolution: {feedback}",
                    "pending",
                )

        return self._update_and_save(ticket_number, mutate)
