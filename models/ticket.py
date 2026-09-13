import uuid
from datetime import datetime


class Ticket:
    """
    Status lifecycle:
    open    -> just raised by the customer, not yet picked up
    pending -> an employee is working it (action_taken/resolution_summary
    describe what's been tried), OR the customer rejected a
    proposed resolution
    closed  -> customer confirmed the issue was solved

    `history` is a running log of every action taken on the ticket, so if
    one employee hands off (or drops off) mid-issue, the next employee who
    opens the ticket by number can see exactly what was tried and why it's
    still pending.
    """

    def __init__(
        self,
        ticket_number=None,
        user_name="",
        user_email="",
        description="",
        assigned_employee=None,
        status="open",
        action_taken="",
        resolution_summary="",
        user_agreed_to_close=None,
        user_feedback="",
        history=None,
        created_at=None,
        updated_at=None,
    ):
        self.ticket_number = ticket_number or self.generate_ticket_number()
        self.user_name = user_name
        self.user_email = user_email
        self.description = description
        self.assigned_employee = assigned_employee
        self.status = status
        self.action_taken = action_taken
        self.resolution_summary = resolution_summary
        self.user_agreed_to_close = user_agreed_to_close
        self.user_feedback = user_feedback
        self.history = history if history is not None else []
        self.created_at = created_at or datetime.now().isoformat(timespec="seconds")
        self.updated_at = updated_at or self.created_at

    @staticmethod
    def generate_ticket_number():
        return "TCK-" + uuid.uuid4().hex[:8].upper()

    def touch(self):
        self.updated_at = datetime.now().isoformat(timespec="seconds")

    def to_dict(self):
        return {
            "ticket_number": self.ticket_number,
            "user_name": self.user_name,
            "user_email": self.user_email,
            "description": self.description,
            "assigned_employee": self.assigned_employee,
            "status": self.status,
            "action_taken": self.action_taken,
            "resolution_summary": self.resolution_summary,
            "user_agreed_to_close": self.user_agreed_to_close,
            "user_feedback": self.user_feedback,
            "history": self.history,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            ticket_number=data.get("ticket_number"),
            user_name=data.get("user_name", ""),
            user_email=data.get("user_email", ""),
            description=data.get("description", ""),
            assigned_employee=data.get("assigned_employee"),
            status=data.get("status", "open"),
            action_taken=data.get("action_taken", ""),
            resolution_summary=data.get("resolution_summary", ""),
            user_agreed_to_close=data.get("user_agreed_to_close"),
            user_feedback=data.get("user_feedback", ""),
            history=data.get("history", []),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
