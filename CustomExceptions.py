# used to report back when a user selects "no" when confirming an operation
class UserCancelledException(Exception):
    def __init__(self, message: str):
        self.message = message

# used when an out-of-range menu option gets past pyip in main.py and is caught by menu.py
class InvalidMenuOptionException(Exception):
    def __init__(self, message: str):
        self.message = message