import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from config.config import BASKETS, strategies, FREQUENCY
from frontend.Datepicker import Datepicker
import tkinter as tk
from stockexchange.FetchStock import FetchStock
from stockexchange.fetch_stock.YFinanceFetcher import YFinanceFetcher
from portfolio.Simulator import Simulator
from config.Parameter import Parameter
from strategies.strategy import Strategy
import numpy as np
import matplotlib.dates as mdates
import pandas as pd
from portfolio.Portfolio import Portfolio
from portfolio.Porrtfoliodispo import Portfoliodispo
from portfolio.SimulatorDispo import SimulatorDispo


class MainFrame(tk.Frame):
    def __init__(self):
        root = tk.Tk()
        root.title("Depository Effect Simulator")
        root.geometry("1200x800")
        self.strategies = strategies
        self.frequency = FREQUENCY

        # Haupt-Frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        # Linker Frame für Plot
        plot_frame = tk.Frame(main_frame)
        plot_frame.pack(side="left", fill="both", expand=True)

        # Rechter Frame für Steuerung
        control_frame = tk.Frame(main_frame, padx=10, pady=10)
        control_frame.pack(side="right", fill="y")

        # Dropdown 1
        strategy_names = [strategy["name"] for strategy in self.strategies]
        dropdown1_var = tk.StringVar(value=strategy_names[0])
        self.dropdown1 = ttk.Combobox(
            control_frame, textvariable=dropdown1_var, values=strategy_names
        )
        self.dropdown1.pack(pady=5)

        # Label für die Eingabe
        label = tk.Label(control_frame, text="Betrag in Euro eingeben:")
        label.pack(pady=10)
        # Eingabefeld
        self.entry = tk.Entry(control_frame)
        self.entry.pack()

        # Label für die Eingabe
        label1 = tk.Label(control_frame, text="Anzahl Aktien:")
        label1.pack(pady=10)
        # Eingabefeld
        self.anzahlAktien = tk.Entry(control_frame)
        self.anzahlAktien.pack()

        # Label für die Eingabe
        label2 = tk.Label(control_frame, text="Dispositionseffektgrenze:")
        label2.pack(pady=10)
        # Eingabefeld
        self.dispoGrenze = tk.Entry(control_frame)
        self.dispoGrenze.pack()

        self.datepicker_from = Datepicker(control_frame, "Datum von", "2025-01-02")
        self.datepicker_to = Datepicker(control_frame, "Datum bis", "2025-05-12")

        # Dropdown 1
        frequency = [frequency["name"] for frequency in self.frequency]
        dropdown_frequency_var = tk.StringVar(value=frequency[0])
        self.dropdown_frequency = ttk.Combobox(
            control_frame, textvariable=dropdown_frequency_var, values=frequency
        )
        self.dropdown_frequency.pack(pady=5)

        # Button
        button = tk.Button(
            control_frame, text="Simulieren", command=self.plot_aktualisieren
        )
        button.pack(pady=10)

        # Matplotlib-Figure im linken Frame
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        plt.xticks(rotation=45, ha="right")
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # --- Matplotlib Navigation Toolbar für Zoom & Pan ---
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

        self.toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        self.toolbar.update()
        self.toolbar.pack(side="bottom", fill="x")

        root.mainloop()

    def plot_aktualisieren(self):
        # Beispiel: Plot je nach Auswahl
        tickers = BASKETS["Nasdaq 100 Tech-Stocks"]

        start_date = self.datepicker_from.date_entry.get()
        end_date = self.datepicker_to.date_entry.get()
        amount = self.entry.get()
        strategyStr = self.dropdown1.get()
        frequency = self.dropdown_frequency.get()
        anzahlAktien = self.anzahlAktien.get()
        dispoGrenze = self.dispoGrenze.get()
        strategy = next(
            (item for item in strategies if item["name"] == strategyStr), None
        )

        parameter = Parameter(
            start_date, end_date, amount, frequency, strategy, anzahlAktien, dispoGrenze
        )

        print(parameter.toString())

        stockexchange = FetchStock(tickers, start_date, end_date, YFinanceFetcher())
        data = stockexchange.fetch_data()
        data.to_csv()

        normalStrategy: Strategy = strategy["strategy"]
        dispoStrategy: Strategy = strategy["strategy_depositoryeffect"]

        normalStrategy.set_StockFetcher(stockexchange)
        dispoStrategy.set_StockFetcher(stockexchange)
        portfolio = Portfolio(amount_start=parameter.amount)
        # Portfolio, das die Aktien und deren Gewichtung enthält
        portfoliodispo = Portfoliodispo(
            amount_start=parameter.amount, anzahl_aktien=parameter.anzahlAktien
        )

        normalPortfolio = Simulator(stockexchange, normalStrategy, parameter, portfolio)
        dispoPortfolio = SimulatorDispo(
            stockexchange, dispoStrategy, parameter, portfoliodispo
        )

        # Ticks um 45 Grad drehen und rechtsbündig ausrichten

        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        # --- Styling für bessere Lesbarkeit ---
        self.ax.set_title("Verbesserter Zeitreihen-Plot", fontsize=16)
        self.ax.set_xlabel("Datum", fontsize=12)
        self.ax.set_ylabel("Wert", fontsize=12)
        self.ax.grid(
            True, linestyle="--", alpha=0.6
        )  # Ein Gitter hilft bei der Orientierung

        normalPortfolio.simulate()
        dispoPortfolio.simulate()

        self.ax.clear()
        self.updateplot(normalPortfolio, "Normal Strategy", "blue")
        self.updateplot(dispoPortfolio, "Dispo Strategy", "orange")
        self.ax.legend()  # Legende nach dem Plotten der Linien aufrufen!
        plt.tight_layout()
        self.canvas.draw()

        # --- 4. Event-Handler-Funktion definieren ---

    def updateplot(self, simulator, strategy, color):

        values = simulator.portfolio.get_values()

        dates = [pd.to_datetime(d) for d in values.keys()]
        (line,) = self.ax.plot(
            dates,
            list(values.values()),
            label=strategy,
            color=color,
        )
        # dispoPortfolio.simulate()
        # values = dispoPortfolio.portfolio.get_values()

        stocks = simulator.portfolio.portfolio

        # Erstellen Sie fiktive Details zu Aktien und Gewichtungen für einige Punkte
        # In einem realen Szenario würden diese Daten aus Ihrer Quelle stammen
        portfolio_details = stocks

        # --- 3. Annotation initialisieren (unsichtbar) ---
        # Erstellen Sie eine leere Annotation, die wir später aktualisieren
        annot = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(20, 20),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.8),
            arrowprops=dict(arrowstyle="->"),
            alpha=0.0,
        )  # Startet unsichtbar

        # --- 5. Event-Listener verbinden ---
        self.fig.canvas.mpl_connect(
            "motion_notify_event",
            lambda event: self.hover(event, line, annot, portfolio_details),
        )
        self.fig.canvas.mpl_connect(
            "axes_leave_event",
            lambda event: self.leave_figure(annot),
        )

    def update_annot(self, ind, line, annot, portfolio_details, event=None):
        # Aktualisiert die Position und den Text der Annotation
        x, y = line.get_data()
        x_pos, y_pos = x[ind["ind"][0]], y[ind["ind"][0]]

        annot.xy = (x_pos, y_pos)

        date_str = pd.to_datetime(x_pos).strftime("%Y-%m-%d")
        details_text = f"Datum: {date_str}\n"

        # Prüfen, ob für dieses Datum Portfolio-Details vorhanden sind
        if pd.Timestamp(x_pos) in portfolio_details:
            portfolio_entry = portfolio_details[pd.Timestamp(x_pos)]
            details_text += f" Amount Buy: {portfolio_entry['amount_buy']} \n"
            if "selled_amount" in portfolio_entry:
                details_text += f"Amount Sell {portfolio_entry['selled_amount']} \n"
            details_text += "\nPortfolio-Zusammensetzung:\n"
            stocks = portfolio_entry["invest"]
            for stock in stocks:
                details_text += f" Ticker: {stock['ticker']}, Amount: {np.round(stock['amount'],2)}, Anzahl: {np.round(stock['shares'],2)}, Price: {np.round(stock['price_buy'],4)} \n"
        else:
            details_text += "\nKeine detaillierten Portfolio-Informationen verfügbar."

        annot.set_text(details_text)
        annot.set_alpha(1.0)  # Sichtbar machen
        if event is not None:
            # Wenn Maus weit rechts/unten, Tooltip nach links/oben verschieben
            if event.x > 800:  # Passe die Schwelle ggf. an Fenstergröße an
                offset_x = -150
            else:
                offset_x = 20
            if event.y > 600:
                offset_y = -100
            else:
                offset_y = 20
            annot.set_position((offset_x, offset_y))
        self.fig.canvas.draw_idle()  # Das Canvas aktualisieren

    def hover(self, event, line, annot, portfolio_details):
        if event.inaxes == self.ax:
            cont, ind = line.contains(event)
            if cont:
                self.update_annot(ind, line, annot, portfolio_details, event)
            else:
                # Maus ist nicht über der Linie, Annotation ausblenden
                if annot.get_alpha() != 0.0:
                    annot.set_alpha(0.0)
                    self.fig.canvas.draw_idle()

    # Optional: Annotation ausblenden, wenn Maus das Diagramm verlässt
    def leave_figure(self, annot):
        annot.set_alpha(0.0)
        annot.set_text("")
        self.fig.canvas.draw_idle()
