import pytest

from utils.ticket_manager import TicketManager


class DummyUser:
    def __init__(self, name, email):
        self.name = name
        self.email = email


@pytest.fixture
def ticket_manager(tmp_path):
    return TicketManager(tickets_file=tmp_path / "tickets.json")


def test_create_ticket(ticket_manager):
    user = DummyUser("Jane Doe", "jane@example.com")
    ticket = ticket_manager.create_ticket(user, "My internet is down")
    assert ticket.status == "open"
    fetched = ticket_manager.get_ticket(ticket.ticket_number)
    assert fetched.description == "My internet is down"


def test_employee_update_then_second_employee_sees_history(ticket_manager):
    user = DummyUser("Jane Doe", "jane@example.com")
    employee1 = DummyUser("Employee One", "emp1@example.com")
    employee2 = DummyUser("Employee Two", "emp2@example.com")

    ticket = ticket_manager.create_ticket(user, "My internet is down")
    ticket_manager.update_ticket(ticket.ticket_number, employee1, "Checking router logs")

    fetched = ticket_manager.get_ticket(ticket.ticket_number)
    assert fetched.status == "pending"
    assert fetched.assigned_employee == "emp1@example.com"
    assert len(fetched.history) == 2  # raised + first update

    # second employee picks it up after the first one drops off
    ticket_manager.update_ticket(ticket.ticket_number, employee2, "Router reset, monitoring")
    fetched_again = ticket_manager.get_ticket(ticket.ticket_number)
    assert len(fetched_again.history) == 3
    assert fetched_again.assigned_employee == "emp2@example.com"
    assert fetched_again.history[1]["by"] == "emp1@example.com"


def test_resolution_confirmed_closes_ticket(ticket_manager):
    user = DummyUser("Jane Doe", "jane@example.com")
    employee = DummyUser("Employee One", "emp1@example.com")

    ticket = ticket_manager.create_ticket(user, "Slow wifi")
    ticket_manager.propose_resolution(ticket.ticket_number, employee, "Upgraded plan")
    ticket_manager.confirm_resolution(ticket.ticket_number, user.email, True)

    fetched = ticket_manager.get_ticket(ticket.ticket_number)
    assert fetched.status == "closed"
    assert fetched.user_agreed_to_close is True


def test_resolution_rejected_keeps_pending(ticket_manager):
    user = DummyUser("Jane Doe", "jane@example.com")
    employee = DummyUser("Employee One", "emp1@example.com")

    ticket = ticket_manager.create_ticket(user, "Slow wifi")
    ticket_manager.propose_resolution(ticket.ticket_number, employee, "Upgraded plan")
    ticket_manager.confirm_resolution(
        ticket.ticket_number, user.email, False, feedback="Still slow in the evenings"
    )

    fetched = ticket_manager.get_ticket(ticket.ticket_number)
    assert fetched.status == "pending"
    assert fetched.user_agreed_to_close is False
    assert fetched.user_feedback == "Still slow in the evenings"
