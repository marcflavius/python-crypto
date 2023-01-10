from time import time
from utils.primeable import Primeable
from utils.printable import Printable
from typing import TypedDict
from member import Member

PrimeTransaction = TypedDict(
    "PrimeTransaction",
    {
        "sender": str,
        "recipient": str,
        "amount": float,
    },
)


class Transaction(Printable, Primeable):
    def __init__(self, transaction: PrimeTransaction):
        self.sender: str = transaction["sender"]
        self.recipient: str = transaction["recipient"]
        self.amount: float = transaction["amount"]
        if hasattr(transaction, "created_at"):
            self.created_at = transaction["created_at"]  # type: ignore
            return
        self.created_at: float = time()

    def __repr__(self):
        return self.__dict__
