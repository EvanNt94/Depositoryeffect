class Parameter:
    def __init__(
        self,
        start_date: str,
        end_date: str,
        amount: str,
        frequency: str,
        strategy,
        anzahlAktien: int,
        dispoGrenze: int,
    ):
        self.strategy = strategy
        # Prüfen, ob anzahlAktien ein int ist, sonst auf 1 setzen
        if anzahlAktien == "" or not isinstance(int(anzahlAktien), int):
            self.anzahlAktien = 3
        else:
            self.anzahlAktien = int(anzahlAktien)
        if amount == "" or not isinstance(int(amount), int):
            self.amount = 1000
        else:
            self.amount = int(amount)

        if dispoGrenze == "" or not isinstance(int(dispoGrenze), int):
            self.dispoGrenze = 0
        else:
            self.dispoGrenze = int(dispoGrenze)

        if frequency == "1 mal am Tag":
            self.frequency = 1
        elif frequency == "1 mal alle 2 Tag":
            self.frequency = 2
        elif frequency == "1 mal in der  Woche":
            self.frequency = 5
        elif frequency == "Alle 4 Wochen":
            self.frequency = 20
        elif frequency == "Alle 6 Monate":
            self.frequency = 120
        else:
            self.frequency = 1
        if start_date == "":
            self.start_date = "2020-01-01"
        else:
            self.start_date = start_date
        if end_date == "":
            self.end_date = "2025-01-01"
        else:
            self.end_date = end_date

    def __str__(self):
        return f"Start-Date: {self.start_date}, end date: {self.end_date}, amount: {self.amount}, frequency: {self.frequency}, strategy: {self.strategy}, AnzahlAktien: {self.anzahlAktien}, Dispogrenze: {self.dispoGrenze}"

    def toString(self):
        print(
            "Start-Date:",
            self.start_date,
            "  end date: ",
            self.end_date,
            "  amount: ",
            self.amount,
            " frequency: ",
            self.frequency,
            "  strategy: ",
            self.strategy,
            " AnzahlAktien: ",
            self.anzahlAktien,
            " Dispogrenze: ",
            self.dispoGrenze,
        )
