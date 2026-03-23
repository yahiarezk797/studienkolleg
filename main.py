from konten import *
from funktionen import *
from argon2 import PasswordHasher

ph = PasswordHasher()


def main():
    print("Willkommen!")
    print("1: Anmelden")
    print("2: Konto eröffnen")
    x = int(input("? "))
    if x == 1:
        id = input("ID: ")
        name = input("Name: ")
        pwd = input("Passwort: ")
        konto = anmelden(id, name, pwd)
        print(konto)
        print(f"Hallo, Frau/Herr {konto.name}\n")
        while True:
            print(f"Geld: {konto.geld}")
            print("1: Geld abheben")
            print("2: Geld überweisen")
            print("3: Geld einzahlen")
            print("4: Kontoverlauf schauen")
            print("5: Konto verlassen")
            y = int(input("? "))
            if y == 1:
                betrag = int(input("Betrag: "))
                geld_abheben(konto, betrag)
            elif y == 2:
                betrag = int(input("Betrag: "))
                id2 = int(input("ID: "))
                konto2 = id_to_konto(id2)
                geld_überweisen(konto, konto2, betrag)
            elif y == 3:
                betrag = int(input("Betrag: "))
                geld_legen(konto, betrag)
            elif y == 4:
                kontoverlauf_schauen(konto)
            elif y == 5:
                break
            else:
                print("Ungültige Anfrage!")
            

    elif x == 2:
        name = input("Name: ")
        pwd1 = input("Passwort: ")
        pwd2 = input("Passwort bestätigen: ")
        if pwd2 != pwd1:
            print("Paswort nicht gleich!")
            return
        pwd = ph.hash(pwd1)

        betrag = input("Betrag: ") 
        print(konto_eröffnen(name, pwd, betrag))

    else:
        print("Ungültige Anfrage!")


if __name__ == "__main__":
    main()