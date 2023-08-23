

class EmailSendingFailedError(Exception):
    def __init__(self, message="Email sending failed."):
        self.message = message
        super().__init__(self.message)
