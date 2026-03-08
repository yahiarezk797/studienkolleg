import os
from pathlib import *
import csv
from accounts import *

def id_gen():
    return len(os.listdir("./accounts")) - 1
    
def creat_an_account(name, pwd, amount):
    id = id_gen()
    data = {"id": id, "name": name, "password": pwd, "money": amount}
    try:
        os.mkdir(os.path.join(f"./accounts/{id}"))
        with open(f"./accounts/{id}/info.csv", "w") as f:
            fields = data.keys()
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerow(data)
        with open("./accounts/accounts.csv", "a") as file:
            fields = data.keys()
            writer = csv.DictWriter(file, fieldnames=fields)
            if id == 0:
                writer.writeheader()
            writer.writerow(data)
        return "The account has been created"
    except Exception as e:
        return e
    
def log_in(id, name, pwd):
    try:
        with open(f"./accounts/{id}/info.csv", "r") as f:
            reader = csv.DictReader(f)
            data = list(reader)[0]
        if name != data["name"]:
            raise Exception("Wrong Name")
        if pwd != data["password"]:
            raise Exception("Wrong Password")
        account = Accounts(data["id"], data["name"], data["password"], data["money"])
        return account
    except Exception as e:
        return e
    