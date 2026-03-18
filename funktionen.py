import os
from pathlib import *
import csv
from konten import *
from datetime import datetime
from main import ph

def id_gen():
    return len(os.listdir("./konten")) - 1
    
def konto_eröffnen(name, pwd, betrag):
    id = id_gen()
    konto = Konten(id, name, pwd, betrag)
    data = {"ID": konto.id, "Name": konto.name, "Passwort": konto.pwd, "Geld": konto.geld}
    try:
        os.mkdir(os.path.join(f"./konten/{id}"))
        with open(f"./konten/{id}/info.csv", "w") as f:
            fields = data.keys()
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerow(data)
        with open("./konten/konten.csv", "a") as file:
            fields = data.keys()
            writer = csv.DictWriter(file, fieldnames=fields)
            if id == 0:
                writer.writeheader()
            writer.writerow(data)
        return f"Erfolgreich!\nID:{id}"
    except Exception as e:
        return e
    
def anmelden(id, name, pwd):
    try:
        if not os.path.exists(f"./konten/{id}"):
            raise Exception("Es gibt keine Konto mit diese ID!")
        with open(f"./konten/{id}/info.csv", "r") as f:
            reader = csv.DictReader(f)
            data = list(reader)[0]
        if name != data["Name"]:
            raise Exception("Falches Name!")
        if not ph.verify(data["Passwort"], pwd):
            raise Exception("Falches Passwort!")
        konto = Konten(data["ID"], data["Name"], data["Passwort"], data["Geld"])
        return konto
    except Exception as e:
        return e
    
def verlauf_ändarn(konto, row):
    with open(f"./konten/{konto.id}/verlauf.csv", "a") as f3:
            writer2 = csv.writer(f3)
            writer2.writerow(row)

def kontos_ändern(konto):
    dict_konto = konto.to_dict()
    with open(f"./konten/{konto.id}/info.csv", "w") as f:
        fields = dict_konto.keys()
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerow(dict_konto)
                           
    with open("./konten/konten.csv", "r") as f1:
        reader = csv.DictReader(f1)
        rows = list(reader)
        rows[konto.id]["Geld"] = konto.geld
            
    with open("./konten/konten.csv", "w") as f2:
        fields = dict_konto.keys()
        writer = csv.DictWriter(f2, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def geld_abheben(konto, betrag):
    try:
        if betrag > konto.geld:
            print("Ihr Geld ist nicht genug!")
            return
        konto.pull(betrag)
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        his = ["Geld abheben", time, betrag]
        kontos_ändern(konto)
        verlauf_ändarn(konto, his)
        print("Erfolgreich!")
    except Exception as e:
        print(e)

def geld_legen(konto, betrag):
    try:
        konto.add(betrag)
        zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = ["Geld legen", zeit, betrag]
        verlauf_ändarn(konto, row)
        kontos_ändern(konto)
        print("Erfolgreich!")
    except Exception as e:
        print(e)

def geld_überweisen(konto1, konto2, betrag):
    try:
        if betrag > konto1.geld:
            print("Ihr Geld ist nicht genug!")
            return
        konto1.überweisen(konto2, betrag)
        zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [f"Geld überweisen von {konto1.id} zu {konto2.id}", zeit, betrag]
        verlauf_ändarn(konto1, row)
        verlauf_ändarn(konto2, row)
        kontos_ändern(konto1)
        kontos_ändern(konto2)
        print("Erfolgreich!")
    except Exception as e:
        print(e)

def kontoverlauf_schauen(konto):
    with open(f"./konten/{konto.id}/verlauf.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
        for row in rows:
            print(row)

def id_to_konto(id):
    try:
        if not os.path.exists(f"./konten/{id}"):
            raise Exception("Es gibt keine Konto mit diese ID!")
        with open(f"./konten/{id}/info.csv", "r") as f:
            reader = csv.DictReader(f)
            data = list(reader)[0]
        konto = Konten(data["ID"], data["Name"], data["Passwort"], data["Geld"])
    except Exception as e:
        print(e)
    return konto