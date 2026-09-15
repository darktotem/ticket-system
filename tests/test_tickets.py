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
    user = DummyUser("Kelvin Muita", "kelvin@example.com")
    ticket = ticket_manager.create_ticket(user, "Logged out of Canvas and cannot log back in.")
    assert ticket.status == "open"
    fetched = ticket_manager.get_ticket(ticket.ticket_number)
    assert fetched.description == "I cannot access my Canvas account"


def test_employee_update_then_second_employee_sees_history(ticket_manager):
    user = DummyUser("Kelvin Muita", "kelvin@example.com")
    employee1 = DummyUser("Employee One", "care1@example.com")
    employee2 = DummyUser("Employee Two", "care2@example.com")

    ticket = ticket_manager.create_ticket(user, "My internet is down")
    ticket_manager.update_ticket(ticket.ticket_number, employee1, "Sending issue to the IT department")

    fetched = ticket_manager.get_ticket(ticket.ticket_number)
    assert fetched.status == "pending"
    assert fetched.assigned_employee == "care1@example.com"
    assert len(fetched.history) == 2  # raised + first update


    # second employee picks it up after the first one drops off
    ticket_manager.update_ticket(ticket.ticket_number, employee2, "Giving you a OTP code to reset your password.")
    fetched_again = ticket_manager.get_ticket(ticket.ticket_number)
    assert len(fetched_again.history) == 3
    assert fetched_again.assigned_employee == "care2@example.com"
    assert fetched_again.history[1]["by"] == "care1@example.com"


def test_resolution_confirmed_closes_ticket(ticket_manager):
    user = DummyUser("Kelvin Muita", "kelvin@example.com")
    employee = DummyUser("Employee One", "care1@example.com")

    ticket = ticket_manager.create_ticket(user, "Slow wifi")
    ticket_manager.propose_resolution(ticket.ticket_number, employee, "Student is logged back in.")
    ticket_manager.confirm_resolution(ticket.ticket_number, user.email, True)

    fetched = ticket_manager.get_ticket(ticket.ticket_number)
    assert fetched.status == "closed"
    assert fetched.user_agreed_to_close is True


def test_resolution_rejected_keeps_pending(ticket_manager):
    user = DummyUser("Kelvin Muita", "kelvin@example.com")
    employee = DummyUser("Employee One", "care1@example.com")

    ticket = ticket_manager.create_ticket(user, "Slow wifi")
    ticket_manager.propose_resolution(ticket.ticket_number, employee, "Student is logged back in.")
    ticket_manager.confirm_resolution(
        ticket.ticket_number, user.email, False, feedback="Unable to log in, the code was invalid."
    )

    fetched = ticket_manager.get_ticket(ticket.ticket_number)
    assert fetched.status == "pending"
    assert fetched.user_agreed_to_close is False
    assert fetched.user_feedback == "Unable to log in, the code was invalid."
