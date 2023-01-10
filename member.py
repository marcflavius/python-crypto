from time import time
from utils.primeable import Primeable
from utils.printable import Printable


class Member(Printable, Primeable):
    def __init__(self, id=None):
        self.members = set([])
        if id is not None:
            self.members.add(id)
    def add(self, id):
        self.members.add(id)
    def all(self):
        return self.members
    def __repr__(self):
        return self.__dict__
