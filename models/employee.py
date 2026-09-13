from models.user import User

class Employee(User):
   role = "employee"
   def __init__(self, name, email, password_hash,department="Customer Care"):
        super().__init__(name, email, password_hash)
        self.department = department
        self._assigned_tickets=[]

def  department(self):
        return self.department

def department(self, value):
        self.department = value
def assigned_tickets(self):
        return self._assigned_tickets

#---methods ---
def assign_ticket(self, ticket_id):
        if ticket_id not in self._assigned_tickets:
            self._assigned_tickets.append(ticket_id)

def to_dict(self):
      data=super().to_dict()
      data.update({
            "type":"Employee",
            "department":self.department,
            "assigned_tickets":self._assigned_tickets
      })
      return data

   


    