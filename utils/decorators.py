from functools import wraps


def login_required(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if self.current_user is None:
            print("Please login first.")
            return None
        return function(self, *args, **kwargs)

    return wrapper


def role_required(*roles):
    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            if self.current_user is None:
                print("log in first.")
                return None
            
            if self.current_user.role not in roles:
                print(f"Access denied, restricted to: {', '.join(roles)}.")
                return None

            return function(self, *args, **kwargs)
        return wrapper
    return decorator

# giving manager super acess. Anaweza fanya whatever the emloyee can.
def employee_required(function):
    return role_required("employee", "manager")(function)

def manager_required(function):
    return role_required("manager")(function)

       