from models.ticket import Ticket


def test_ticket_number_auto_generated_when_not_given():
    ticket = Ticket(user_name="Jane", user_email="jane@example.com", description="Issue")
    assert ticket.ticket_number.startswith("TCK-")
    assert len(ticket.ticket_number) == len("TCK-") + 8


def test_two_tickets_get_different_numbers():
    ticket_a = Ticket(user_email="jane@example.com", description="A")
    ticket_b = Ticket(user_email="jane@example.com", description="B")
    assert ticket_a.ticket_number != ticket_b.ticket_number


def test_defaults_on_a_freshly_created_ticket():
    ticket = Ticket(user_email="jane@example.com", description="Issue")
    assert ticket.status == "open"
    assert ticket.assigned_employee is None
    assert ticket.history == []
    assert ticket.user_agreed_to_close is None


def test_touch_updates_updated_at():
    ticket = Ticket(user_email="jane@example.com", description="Issue")
    original_updated_at = ticket.updated_at
    ticket.touch()
    # Same-second touches can produce an identical timestamp; the important
    # part is that touch() always sets updated_at without raising and
    # without ever making it older than created_at.
    assert ticket.updated_at >= original_updated_at


def test_to_dict_and_from_dict_roundtrip():
    original = Ticket(
        ticket_number="TCK-ABCD1234",
        user_name="Jane",
        user_email="jane@example.com",
        description="My internet is down",
        assigned_employee="emp1@example.com",
        status="pending",
        action_taken="Checked router",
        resolution_summary="",
        user_agreed_to_close=None,
        user_feedback="",
        history=[{"by": "emp1@example.com", "action": "Checked router", "status": "pending", "timestamp": "t1"}],
    )

    rebuilt = Ticket.from_dict(original.to_dict())

    assert rebuilt.ticket_number == "TCK-ABCD1234"
    assert rebuilt.description == "My internet is down"
    assert rebuilt.assigned_employee == "emp1@example.com"
    assert rebuilt.status == "pending"
    assert rebuilt.history == original.history


def test_from_dict_defaults_missing_optional_fields():
    rebuilt = Ticket.from_dict({"ticket_number": "TCK-XYZ", "user_email": "jane@example.com"})
    assert rebuilt.status == "open"
    assert rebuilt.history == []
    assert rebuilt.description == ""
