from time import time


class Block:
    def __init__(self, block):
        self.index = block["index"]
        self.previous_hash = block["previous_hash"]
        self.transactions = block["transactions"]
        self.salt = block["salt"]
        if hasattr(block, 'created_at'):
            self.created_at = block["created_at"]
            return 
        self.created_at = time()
    def __repr__(self):
        return self.__dict__

