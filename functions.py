import os
from pathlib import *
import csv
from accounts import *
from datetime import datetime

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
        return f"The account has been created\nID:{id}"
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
    
def pull_money(acc, amount):
    try:
        if amount > acc.money:
            print("Ihr Geld ist nicht genug")
            return
        acc.pull(amount)
        dict_acc = acc.to_dict()
        with open(f"./accounts/{acc.id}/info.csv", "w") as f:
            fields = dict_acc.keys()
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerow(dict_acc)
                
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        his = ["Pulling money", time, amount]
        with open("./accounts/accounts.csv", "r") as f1:
            reader = csv.DictReader(f1)
            rows = list(reader)
            rows[acc.id]["money"] = acc.money
        
        with open("./accounts/accounts.csv", "w") as f2:
            fields = dict_acc.keys()
            writer = csv.DictWriter(f2, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

        with open(f"./accounts/{acc.id}/history.csv", "a") as f3:
            writer2 = csv.writer(f3)
            writer2.writerow(his)
        
        print("Erfolgreich!")
    except Exception as e:
        print(e)
    