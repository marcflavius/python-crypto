from time import time
from utils.printable import Printable


class Member(Printable):
    
    def __init__(self):
        self.members = set([])
    def add(self, id):
        self.members.add(id)
    def all(self):
        return self.members
    def __repr__(self):
        return self.__dict__
