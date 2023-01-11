from time import time
from typing import TypedDict
from utils.primeable import Primeable
from utils.printable import Printable
from transaction import Transaction

PrimeBlock = TypedDict(
    "PrimeBlock",
    {"index": int, "previous_hash": str, "transactions": list, "salt": int},
)


class Block(Printable, Primeable):
    def __init__(self, block: PrimeBlock):
        self.index = block["index"]
        self.previous_hash = block["previous_hash"]
        self.transactions = block["transactions"]
        self.salt = block["salt"]
        if hasattr(block, "created_at"):
            self.created_at = block["created_at"]  # type: ignore
            return
        self.created_at = time()

    def __repr__(self):
        return self.__dict__

    def to_prime(self):
        prime_transactions = []
        if self.transactions == []:
            return []
        for transaction in self.transactions:
            if type(transaction) == Transaction:
                prime_transactions.append(transaction.to_prime())
            else:
                prime_transactions.append(transaction)
        self.transactions = prime_transactions
        return self.__dict__
