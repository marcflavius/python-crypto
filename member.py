from time import time


class Member:
    
    def __init__(self):
        self.members = set([])

    def add(self, id):
        self.members.add(id)
    
    def all(self):
        return self.members
    def __repr__(self):
        return self.__dict__
