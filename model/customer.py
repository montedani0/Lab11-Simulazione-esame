from dataclasses import dataclass


@dataclass
class Customer:
    CustomerId : int
    FirstName : str
    LastName : str
    Country : str

    def __hash__(self):
        return hash(self.CustomerId)

    def __eq__(self, other):
        return self.CustomerId == other.CustomerId

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"