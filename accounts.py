class Accounts:
    def __init__(self, id, name,pwd, money):
        if int(money) < 0:
            raise ValueError("Das Betrag soll positiv sein.")
        self.id = int(id)
        self.name = name
        self.pwd = pwd
        self.money = int(money)

    def __eq__(self, acc):
        return (self.pwd == acc.pwd and self.id == acc.id and self.name == acc.name)
    
    def trans(self, acc, amount):
        if amount <= 0:
            raise ValueError("Das Betrag soll positiv sein.")
        if self.money < amount:
            return False
        self.money -= amount
        acc.money += amount
        return True

    def add(self, amount):
        if amount <= 0:
            raise ValueError("Das Betrag soll positiv sein.")
        self.money += amount

    def pull(self, amount):
        if amount <= 0:
            raise ValueError("Das Betrag soll positiv sein.")
        self.money -= amount

    def __repr__(self):
        return f"Name: {self.name}\nMoney: {self.money}"
    
    def to_dict(self):
        return {"id": self.id ,"name": self.name, "password": self.pwd, "money": self.money}