import tkinter as tk
from tkinter.ttk import Combobox
from datetime import datetime
from tkcalendar import DateEntry


class Datepicker:
    def __init__(self, parent: tk.Tk, label: tk.Label, date: str):
        self.parent = parent
        self.label = label
        self.initDate = date
        self.date_var = tk.StringVar()
        self.date_var.set(date)
         # Label für die Eingabe
        label = tk.Label(self.parent, text=self.label)
        label.pack(pady=10)
        self.date_entry = tk.Entry(self.parent, textvariable=self.date_var)
        self.date_entry.pack()


    def datum_anzeigen():
        ausgewaehlt = cal.get_date()
        label.config(text=f"Ausgewähltes Datum: {ausgewaehlt}")

        root = tk.Tk(self.parent)
        root.title("Datepicker Beispiel")
        root.geometry("300x150")

        # DateEntry (Kalenderfeld)
        cal = DateEntry(root, date_pattern='yyyy-mm-dd')
        cal.pack(pady=10)

        # Button zum Auslesen
        button = tk.Button(root, text="Datum anzeigen", command=datum_anzeigen)
        button.pack(pady=5)

        # Label für die Ausgabe
        label = tk.Label(root, text="")
        label.pack()
