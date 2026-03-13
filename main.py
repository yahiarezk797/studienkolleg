from accounts import *
from functions import *


def main():
    print("Willkommen!")
    print("1: Anmelden")
    print("2: Konto eröffnen")
    x = int(input("? "))
    if x == 1:
        id = input("ID: ")
        name = input("Name: ")
        pwd = input("Passwort: ")
        acc = log_in(id, name, pwd)
        print(f"Hallo, Frau/Herr {acc.name}\n")
        print("1: Pull money")
        print("2: Transfer money")
        print("3: Put money")
        print("4: See account's history")
        y = int(input("? "))
        if y == 1:
            amount = int(input("Betrag: "))
            pull_money(acc, amount)
    else:
        name = input("Name: ")
        pwd = input("Passwort: ")
        amount = input("Betrag: ") 
        print(creat_an_account(name, pwd, amount))


if __name__ == "__main__":
    main()