# ADMIN and CUSTOMER
class Users:
    def __init__(self, email: str, password: str, status: str) -> None:
        self.email = email
        self.password = password
        self.status = status


class Medicine:
    def __init__(self, med_name: str, price: int, description: str, formula: str, quantity: int) -> None:
        self.med_name = med_name
        self.price = price
        self.description = description
        self.formula = formula
        self.quantity = quantity


class Prescription:
    def __init__(self, med_name: str, quantity: int) -> None:
        self.med_name, self.quantity = med_name, quantity


class Order:
    def __init__(self, med_name, quantity, price):
        self.med_name, self.quantity, self.price = med_name, quantity, price
