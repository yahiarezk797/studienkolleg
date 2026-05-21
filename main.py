from konten import *
from funktionen import *
from argon2 import PasswordHasher
from getpass import getpass


ph = PasswordHasher()


def main():
    while True:
        try:
            print("Willkommen!")
            print("XD-Bank")
            print("1: Anmelden")
            print("2: Konto eröffnen")
            print("3: Passwort vergessen")
            print("4: Program verlassen")
            x = input("? ")
            if x == "1":
                id = input("ID: ")
                name = input("Name: ")
                versuchen = 0
                while True:
                    versuchen += 1
                    pwd = getpass("Passwort: ")
                    konto = anmelden(id, name, pwd)
                    if type(konto) == Konten:
                        versuchen = 0
                        break
                    if versuchen == 3:
                        konto = id_to_konto(id)
                        email_schicken(konto.email, "Wichtige Sicherheitsbenachrichtigung für Ihr Konto", konstanten.versuchen_text)
                        return                
                print(f"Hallo, Frau/Herr {konto.name}\n")
                while True:
                    print(f"Geld: {konto.geld}")
                    print("1: Geld abheben")
                    print("2: Geld überweisen")
                    print("3: Geld einzahlen")
                    print("4: Kontoverlauf zeigen")
                    print("5: Passwort ändarn")
                    print("6: Grenzen des Abhebens ändern")
                    print("7: Die Angebote zeigen")
                    print("8: Konto verlassen")
                    y = input("? ")
                    if y == "1":
                        betrag = int(input("Betrag: "))
                        geld_abheben(konto, betrag)
                    elif y == "2":
                        betrag = int(input("Betrag: "))
                        id2 = int(input("ID: "))
                        konto2 = id_to_konto(id2)
                        geld_überweisen(konto, konto2, betrag)
                    elif y == "3":
                        betrag = int(input("Betrag: "))
                        geld_legen(konto, betrag)
                    elif y == "4":
                        kontoverlauf_schauen(konto)
                    elif y == "5":
                        passwort_ändarn(konto.id)
                    elif y == "6":
                        while True:
                            betrag = int(input("Grenzwert: "))
                            if betrag < 0:
                                print("Das Betrag kann nicht negativ sein")
                                continue
                            if betrag <= 30000:
                                break
                            print("Das Grenzwert soll kleiner oder gleich 30000 sein!")
                        grenzen_ändern(konto, betrag)
                    elif y == "7":
                        angeboten_zeigen()
                    elif y == "8":
                        break
                    else:
                        print("Ungültige Anfrage!")
                    print("\n\n")                    
            elif x == "2":
                name = input("Name: ")
                email = input("E-Mail: ")
                pwd1 = getpass("Passwort: ")
                while True:
                    pwd2 = getpass("Passwort bestätigen: ")
                    if pwd1 == pwd2:
                        break
                    print("Paswort nicht gleich!")
                pwd = ph.hash(pwd1)

                betrag = input("Betrag: ") 
                print(konto_eröffnen(name, pwd, betrag, email))            
            elif x == "3":
                id = int(input("ID: "))
                passwort_ändarn(id)
            elif x == "4":
                break
            else:
                print("Ungültige Anfrage!")
        except Exception:
            pass
        print("\n\n")

if __name__ == "__main__":
    main()