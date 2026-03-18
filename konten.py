

class Konten:
    def __init__(self, id, name,pwd, geld):
        if int(geld) < 0:
            raise ValueError("Das Betrag kann nicht negativ sein")
        self.id = int(id)
        self.name = name
        self.pwd = pwd
        self.geld = int(geld)

    def __eq__(self, konto):
        return (self.pwd == konto.pwd and self.id == konto.id and self.name == konto.name)
    
    def überweisen(self, konto, betrag):
        if betrag <= 0:
            raise ValueError("Das Betrag kann nicht negativ sein")
        if self.geld < betrag:
            return False
        self.geld -= betrag
        konto.geld += betrag
        return True

    def add(self, betrag):
        if betrag <= 0:
            raise ValueError("Das Betrag kann nicht negativ sein")
        self.geld += betrag

    def pull(self, betrag):
        if betrag <= 0:
            raise ValueError("Das Betrag kann nicht negativ sein")
        self.geld -= betrag

    def __repr__(self):
        return f"Name: {self.name}\nGeld: {self.geld}"
    
    def to_dict(self):
        return {"ID": self.id ,"Name": self.name, "Passwort": self.pwd, "Geld": self.geld}