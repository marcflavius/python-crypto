class Printable():
    def __str__(self) -> str:
        return self.__dict__.__str__()