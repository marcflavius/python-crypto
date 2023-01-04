from time import time
from typing import Optional, TypedDict
from utils.printable import Printable

PrimeBlock = TypedDict('PrimeBlock', {'index': int, 'previous_hash': str, 'transactions': list, 'salt': int})

class Block(Printable):
    def __init__(self, block: PrimeBlock):
        self.index = block["index"]
        self.previous_hash = block["previous_hash"]
        self.transactions = block["transactions"]
        self.salt = block["salt"]
        if hasattr(block, 'created_at'):
            self.created_at = block["created_at"] # type: ignore
            return 
        self.created_at = time()
    def __repr__(self):
        return self.__dict__
    def to_prime(self):
        return self.__dict__

