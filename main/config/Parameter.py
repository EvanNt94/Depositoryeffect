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
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.strategy = strategy
        # Prüfen, ob anzahlAktien ein int ist, sonst auf 1 setzen
        if anzahlAktien == "" or anzahlAktien is not isinstance(int(anzahlAktien), int):
            self.anzahlAktien = 3
        else:
            self.anzahlAktien = int(anzahlAktien)
        if amount == "" or amount is not isinstance(int(amount), int):
            self.amount = 1000
        else:
            self.amount = int(amount)
        self.dispoGrenze = dispoGrenze

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
