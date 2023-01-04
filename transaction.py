from time import time
from utils.printable import Printable


class Transaction(Printable):
    def __init__(self, transaction):
        self.sender = transaction["sender"]
        self.recipient = transaction["recipient"]
        self.amount = transaction["amount"]
        if hasattr(transaction, 'created_at'):
            self.created_at = transaction["created_at"]
            return 
        self.created_at = time()
    def __repr__(self):
        return self.__dict__
 