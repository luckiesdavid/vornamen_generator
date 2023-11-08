import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
import os
import glob
from datetime import datetime
import pyphen
import random

# Liste von Namen
csv_in = 'vornamen2020_opendata.csv'
csv_out = 'Favoriten/Favorites_'
namen = []
namen_out = {'Name': [], 'Bewertung': []}
# namen = ["Simon", "Isabelle", "Nathan", "Melanie", "Alex"]
aktueller_index = 0
fav_csv_in = "Favoriten/Favorites_18_23_58.csv"
#fav_csv_in = csv_out + t +".csv"
fav_namen = []
dict_silben = {'1': [], '2': [], '3': [], '4': []}


def import_fav_names(fav_csv_in):
    global fav_namen
    # fixe CSV-Datei einlesen
    #df = pd.read_csv(fav_csv_in, encoding='ISO-8859-1')

    # neuste CSV-Datei einlesen
    dateien = glob.glob(os.path.join("Favoriten", '*'))
    dateien.sort(key=os.path.getctime)
    neueste_datei = dateien[-1]
    print("eingelesene Datei:", neueste_datei)
    df = pd.read_csv(neueste_datei, encoding='ISO-8859-1')

    # 2 = daumen hoch; 1 = daumen mitte; 0 = daumen runter
    bedingung = df.iloc[:, 2].astype(str).str.contains('2', case=False, na=False)
    namen_hoch = df.loc[bedingung, df.columns[1]]
    for i in namen_hoch:
        fav_namen.append(i)
        #print(namen)
    return fav_namen


def silbentrennung(fav_namen):
    dic = pyphen.Pyphen(lang='de')
    #dict_silben.clear()
    #dict_silben = {'1': [], '2': [], '3': [], '4': []}
    # check ob dictionary schon beschrieben
    if len(dict_silben["1"]) == 0:
        for i in fav_namen:
            silben = dic.inserted(i).split('-')
            if len(silben) == 0:
                print("alle durchiteriert")
            if len(silben) == 1:
                dict_silben["1"].append(silben[0])
            if len(silben) == 2:
                dict_silben["1"].append(silben[0])
                dict_silben["2"].append(silben[1])
            if len(silben) == 3:
                dict_silben["1"].append(silben[0])
                dict_silben["2"].append(silben[1])
                dict_silben["3"].append(silben[2])
            if len(silben) == 4:
                dict_silben["1"].append(silben[0])
                dict_silben["2"].append(silben[1])
                dict_silben["3"].append(silben[2])
                dict_silben["4"].append(silben[3])
            else:
                print("")
    print('1_DICT_SILBEN:',dict_silben)
    print('2_DICT_SILBEN:',dict_silben)


def silben_zusammenfuegen1(d):
    zufaellige_silben = []
    for i in range(1, 5):
        if d.get(str(i)):
            zufaellige_silbe = random.choice(d[str(i)])
            zufaellige_silben.append(zufaellige_silbe)
    return ''.join(zufaellige_silben)


#def silben_zusammenfuegen2(dict_silben):
#    print(dict_silben)
#    generierter_name = silben_zusammenfuegen1(dict_silben)
#    print("Gererierter Name:", generierter_name)

def start_gen():
    import_names(csv_in)
    silbentrennung(fav_namen)
    print('DICT_SILBEN:',dict_silben)
    generierter_name = silben_zusammenfuegen1(dict_silben)
    print("Gererierter Name:", generierter_name)
    label_gen.config(text=generierter_name)


def import_names(csv_in):
    global namen
    # CSV-Datei einlesen
    df = pd.read_csv(csv_in, encoding='ISO-8859-1')
    # Bedingte Auswahl: Nur Zeilen, in denen in der dritten Spalte der Buchstabe "m" enthalten ist
    bedingung = df.iloc[:, 2].str.contains('m', case=False, na=False)
    jungennamen = df.loc[bedingung, df.columns[0]]
    for i in jungennamen:
        namen.append(i)
    return namen


def export_names(csv_out, names_out):
    global t
    if len(names_out["Name"]) == 0:
        print("...Dictonary ist leer\nNamensanzahl:", len(names_out["Name"]))
    else:
        df = pd.DataFrame.from_dict(names_out)#, orient="index")
        t = datetime.now().strftime("%H_%M_%S")
        df.to_csv(csv_out + t +".csv")
        print("Exportiere (Dictionary)/Favoriten in CSV...")



def button_geklickt():
    global aktueller_index, namen
    print(namen)
    label.config(text=namen[aktueller_index])
    aktueller_index += 1
    if aktueller_index >= len(namen):
        aktueller_index = 0  # Zurücksetzen auf den Anfang der Liste


def aktualisiere_label():
    global aktueller_index, label
    label.config(text=namen[aktueller_index])
    aktueller_index += 1
    if aktueller_index >= len(namen):
        aktueller_index = 0  # Zurücksetzen auf den Anfang der Liste


def daumenhoch():
    aktualisiere_label()
    namen_out["Name"].append(namen[aktueller_index-2])
    namen_out["Bewertung"].append("2")
#    print(aktueller_index)
#    print(namen[aktueller_index])
#    print(namen[aktueller_index-2])
    print(namen_out)


def daumenrunter():
    aktualisiere_label()
    namen_out["Name"].append(namen[aktueller_index-2])
    namen_out["Bewertung"].append("0")
    print(namen_out)


def daumenmitte():
    aktualisiere_label()
    namen_out["Name"].append(namen[aktueller_index-2])
    namen_out["Bewertung"].append("1")
    print(namen_out)


def tkinter():
    global label, label_gen
    # Tkinter-Fenster erstellen
    fenster = tk.Tk()
    fenster.title("Bewertung Vornamen")
    fenster.geometry("400x350")
    icon_size = 40

    label = tk.Label(fenster, text="", font=("Helvetica", 36))
    label.pack()

    aktualisieren_button = tk.Button(fenster, text="Nächster Wert", command=aktualisiere_label)
    aktualisieren_button.pack()

    # Frame für Horizontale Anordnung von Buttons
    button_frame = tk.Frame(fenster)
    button_frame.pack()

    daumen_hoch = Image.open(r"icons/daumen-hoch.png")
    daumen_hoch = daumen_hoch.resize((icon_size, icon_size), Image.LANCZOS)
    daumen_hoch = ImageTk.PhotoImage(daumen_hoch)
    daumen_hoch_button = tk.Button(button_frame, image=daumen_hoch, command=daumenhoch)
    daumen_hoch_button.pack(side=tk.LEFT, padx=10, pady=30)

    daumen_mitte = Image.open(r"icons/daumen-mitte.png")
    daumen_mitte = daumen_mitte.resize((icon_size, icon_size), Image.LANCZOS)
    daumen_mitte = ImageTk.PhotoImage(daumen_mitte)
    daumen_mitte_button = tk.Button(button_frame, image=daumen_mitte, command=daumenmitte)
    daumen_mitte_button.pack(side=tk.LEFT, padx=10, pady=30)

    daumen_runter = Image.open(r"icons/daumen-runter.png")
    daumen_runter = daumen_runter.resize((icon_size, icon_size), Image.LANCZOS)
    daumen_runter = ImageTk.PhotoImage(daumen_runter)
    daumen_runter_button = tk.Button(button_frame, image=daumen_runter, command=daumenrunter)
    daumen_runter_button.pack(side=tk.LEFT, padx=10, pady=30)

    export_button = tk.Button(fenster, text="Export", command=lambda: export_names(csv_out, namen_out))
    export_button.pack()

    import_button = tk.Button(fenster, text="Import", command=lambda: import_fav_names(fav_csv_in))
    import_button.pack()

    gen_button = tk.Button(fenster, text="Generator", command=start_gen)
    gen_button.pack()

    label_gen = tk.Label(fenster, text="", font=("Helvetica", 36))
    label_gen.pack()

    schliessen_button = tk.Button(fenster, text="Schließen", command=fenster.destroy)
    schliessen_button.pack()

    fenster.mainloop()


if __name__ == "__main__":
    import_names(csv_in)
    tkinter()
    export_names(csv_out, namen_out)
    import_fav_names(fav_csv_in)
    silbentrennung(fav_namen)
    #silben_zusammenfuegen2()