import os
from pathlib import *
import csv
from konten import *
from datetime import datetime
from main import ph
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import random
from getpass import getpass
import konstanten

def id_gen():
    return len(os.listdir("./konten")) - 1
    
def konto_eröffnen(name, pwd, betrag, email):
    id = id_gen()
    konto = Konten(id, name, pwd, betrag, email)
    data = konto.to_dict()
    try:
        os.mkdir(os.path.join(f"./konten/{id}"))
        konto_zum_info(data)
        with open("./konten/konten.csv", "a") as file:
            fields = data.keys()
            writer = csv.DictWriter(file, fieldnames=fields)
            if id == 0:
                writer.writeheader()
            writer.writerow(data)
        konto_zum_sicherheitsinfo(konto)
        with open(f"./konten/{id}/verlauf.csv", "w") as f1:
            pass
        return f"Erfolgreich!\nID:{id}"
    except Exception as e:
        print(e)

def check_passwort(hpwd, pwd):
    try:
        ph.verify(hpwd, pwd)
        return True
    except Exception:
        return False

def anmelden(id, name, pwd):
    try:
        if not os.path.exists(f"./konten/{id}"):
            raise Exception("Es gibt keine Konto mit diese ID!")
        with open(f"./konten/{id}/info.csv", "r") as f:
            reader = csv.DictReader(f)
            data = list(reader)[0]
        if name != data["Name"]:
            raise Exception("Falches Name!")
        if not check_passwort(data["Passwort"], pwd):
            raise Exception("Falches Passwort!")
        with open(f"./konten/{id}/sicherheitsinfo.csv", "r") as f:
            reader = csv.DictReader(f)
            data2 = list(reader)[0]
        konto = Konten(data["ID"], data["Name"], data["Passwort"], data["Geld"], data2["E-Mail"], int(data2["Grenzwert"]))
        return konto
    except Exception as e:
        print(e)
    
def verlauf_ändarn(konto, row):
    with open(f"./konten/{konto.id}/verlauf.csv", "a") as f3:
            writer2 = csv.writer(f3)
            writer2.writerow(row)

def kontos_ändern(konto, was):
    dict_konto = konto.to_dict()
    konto_zum_info(dict_konto)
                           
    with open("./konten/konten.csv", "r") as f1:
        reader = csv.DictReader(f1)
        rows = list(reader)
        if was == "Geld":
            rows[konto.id][was] = konto.geld
        if was == "Passwort":
            rows[konto.id][was] = konto.pwd
            
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
        zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if (geld_abheben_heute(konto.id, zeit.split(" ")[0]) + betrag) > konto.grenzwert:
            defrenz = konto.grenzwert - geld_abheben_heute(konto.id, zeit.split(" ")[0])
            if defrenz <= 0:
                print("Sie können Heute kein Geld abheben!")
                return
            print(f"Sie können Heute nur {defrenz} abheben!")
            return
        konto.pull(betrag)
        his = ["Geld abheben", zeit, betrag]
        kontos_ändern(konto, "Geld")
        verlauf_ändarn(konto, his)
        print("Erfolgreich!")
    except Exception as e:
        print(e)

def geld_legen(konto, betrag):
    try:
        konto.add(betrag)
        zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = ["Geld einzahlen", zeit, betrag]
        verlauf_ändarn(konto, row)
        kontos_ändern(konto, "Geld")
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
        kontos_ändern(konto1, "Geld")
        kontos_ändern(konto2, "Geld")
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
        with open(f"./konten/{id}/sicherheitsinfo.csv", "r") as f1:
            reader = csv.DictReader(f1)
            data2 = list(reader)[0]
        konto = Konten(data["ID"], data["Name"], data["Passwort"], data["Geld"], data2["E-Mail"], int(data2["Grenzwert"]))

    except Exception as e:
        print(e)
    return konto

def code_gen():
    code = random.randint(10**7, 10**8 - 1)
    return code

def code_schicken(id,code):
    konto = id_to_konto(id)
    text = f"Code: {code}"
    email_schicken(konto.email, "Das Passwort ändarn", text)

def email_schicken(email,sub, text):
    msg = MIMEMultipart()
    msg["From"] = "yahiarezk797@gmail.com"
    msg["To"] = email
    msg["Subject"] = sub

    msg.attach(MIMEText(text, "plain"))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("yahiarezk797@gmail.com", "nzqj gqdy xsdk ubcb")
        server.sendmail("yahiarezk797@gmail.com", email, msg.as_string())
    
    print("✅ Email ist erfolgreich geschickt!")

def passwort_ändarn(id):
    code = code_gen()
    code_schicken(id, code)
    x = int(input("Code: ").strip())
    if x == code:
        konto = id_to_konto(id)
        pwd1 = getpass("Passwort: ")
        while True:
            pwd2 = getpass("Passwort bestätigen: ")
            if pwd1 == pwd2:
                break
            print("Paswort nicht gleich!")
        pwd = ph.hash(pwd1)
        konto.pwd = pwd
        dict_konto = konto.to_dict()
        konto_zum_info(dict_konto)
                            
        kontos_ändern(konto, "Passwort")
        
        
        print("Erfolgreich!")

    else:
        print("Das Code war falch!")

def geld_abheben_heute(id, zeit):
    with open(f"./konten/{id}/verlauf.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
    geld = 0      
    for row in rows:
        if row[0] != "Geld abheben":
            continue
        time2 = row[1].split(" ")[0]
        if time2 == zeit:
            geld += int(row[2])
    return geld

def grenzen_ändern(konto, betrag):
    konto.grenzwert = betrag
    konto_zum_sicherheitsinfo(konto)

def konto_zum_sicherheitsinfo(konto):
    row = konto.to_dict2()
    with open(f"./konten/{konto.id}/sicherheitsinfo.csv", "w") as f2:
        fields = row.keys()
        writer = csv.DictWriter(f2, fieldnames=fields)
        writer.writeheader()
        writer.writerow(row)

def konto_zum_info(dict_konto):
    with open(f"./konten/{dict_konto["ID"]}/info.csv", "w") as f:
            fields = dict_konto.keys()
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerow(dict_konto)

def angeboten():
    random_gechäfte = random.sample(konstanten.gechäfte, 5)
    ang = random.choices(range(5, 26), k=5)
    text = ""
    for i in range(5):
        text += f"{random_gechäfte[i]}: -{ang[i]}%\n\n"
    return text
def angeboten_zeigen():
    print(angeboten())