class UserDoesntExist(Exception):
    # Raised when operation involving a user is attempted and user doesn't exist
    def __init__(self, message="This User doesn't exist"):
        self.message = message
        super().__init__(self.message)
class AppointmentDoesntExist(Exception):
    # Raised when an operation involving an appointment is attempted and the appointment doesn't exist
    def __init__(self, message="This Appointment doesn't exist"):
        self.message = message
        super().__init__(self.message)
    
class UserExists(Exception):
    # Raised when a user is attempted to be created but already exists in the cluster
    def __init__(self, message="This user already exists"):
        self.message = message
        super().__init__(self.message)