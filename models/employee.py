from models.user import User

@classmethod
class Employee(User):
   role = "employee"
   def __init__(self, name, email, password_hash,department="Customer Care"):
        super().__init__(name, email, password_hash)
        self.department = department
        self._assigned_tickets=[]
         
@property
def  department(self):
        return self.department

@department.setter
def department(self, value):
     if not value or not isinstance(value, str):
            raise ValueError("Department must be a non-empty string.")    
     self._department = value

@property
def assigned_tickets(self):
        return list(self._assigned_tickets)

@property
def ticket_count(self):
        return len(self._assigned_tickets)


#---methods ---
def assign_ticket(self, ticket_id):
        if ticket_id  in self._assigned_tickets:
           print(f"[!] Ticket {ticket_id} is already assigned to {self.name}.")

           return False
        self._assigned_tickets.append(ticket_id)
        print(f"[+] Ticket {ticket_id} assigned to {self.name}.") 

        return True

def resolve_ticket(self, ticket_id):
        if ticket_id not in self._assigned_tickets:
            print(f"[!] Ticket {ticket_id} is not in your queue.")

            return False
        self._assigned_tickets.remove(ticket_id)
        print(f"[✓] Ticket {ticket_id} resolved by {self.name}.")
        return True        
#serialization

def to_dict(self):
      data=super().to_dict()
      data.update({
            "type":"Employee",
            "department":self._department,
            "assigned_tickets":self._assigned_tickets
      })
      return data

@classmethod
def from_dict(cls, data):
      name=data.get("name")
      email=data.get("email")
      password_hash=data.get("password_hash")
      department=data.get("department","Customer Care")
      employee=cls(name,email,password_hash,department)
      employee._assigned_tickets=data.get("assigned_tickets",[])
      return employee


   

