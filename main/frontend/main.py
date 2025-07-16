import json
import os
import time
import tkinter as tk
from datetime import date
from tkinter import ttk

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from config.baskets.main import BASKETS
from config.config import FREQUENCY, strategies
from config.Parameter import Parameter
from frontend.Datepicker import Datepicker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from portfolio.Porrtfoliodispo import Portfoliodispo
from portfolio.PorrtfolioUngewichtet import PortfolioUngewichtet
from portfolio.Portfolio import Portfolio
from portfolio.Simulator import Simulator
from portfolio.SimulatorDispo import SimulatorDispo
from results.config import result_path
from stockexchange.fetch_stock.YFinanceFetcher import YFinanceFetcher
from stockexchange.FetchStock import FetchStock
from strategies.buy_hold_strategy import BuyHoldStrategy
from strategies.metrics import calc_diff_disp_norm
from strategies.strategy import Strategy


class MainFrame(tk.Frame):
    def __init__(self):
        self.root = None
        self.stock_exchange = None
        self.normalSimulator: Simulator = None
        self.dispoSimulator: Simulator = None
        self.buyHoldSimulator: Simulator = None
        self.start_plot()

    def start_plot(self):
        root = tk.Tk()
        self.root = root
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

        # Dropdown Basket
        basket_names = [list(item.keys())[0] for item in BASKETS]
        print(basket_names)
        dropdown2_var = tk.StringVar(value=basket_names[0])
        self.dropdown2 = ttk.Combobox(
            control_frame, textvariable=dropdown2_var, values=basket_names
        )
        self.dropdown2.pack(pady=5)

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

    def plot_normal_strategy(self, parameter: Parameter):
        portfolio = Portfoliodispo(parameter.amount, parameter.anzahlAktien)

        parameter["strategy"].set_StockFetcher(self.stock_exchange)
        simulator = Simulator(
            self.stock_exchange, parameter["strategy"], parameter, portfolio
        )
        simulator.simulate()
        self.normalSimulator = simulator
        self.updateplot(
            simulator,
            f" {simulator.strategy.strategy_name} Strategy",
            "blue",
        )

    def plot_dispo_strategy(self, parameter: Parameter):
        portfolio = Portfolio(amount_start=parameter.amount)

        parameter["strategy"].set_StockFetcher(self.stock_exchange)
        simulator = Simulator(
            self.stock_exchange, parameter["strategy"], parameter, portfolio
        )
        simulator.simulate()
        self.dispoSimulator = simulator
        self.updateplot(
            simulator,
            f" {simulator.strategy.strategy_name} Strategy",
            "red",
        )

    def plot_buy_and_hold_weighted_strategy(self, parameter: Parameter):
        portfolio = Portfolio(parameter.amount)

        strategy = BuyHoldStrategy()
        strategy.set_StockFetcher(self.stock_exchange)
        simulator = Simulator(self.stock_exchange, strategy, parameter, portfolio)
        simulator.simulate()
        self.buyHoldSimulator = simulator
        self.updateplot(
            simulator,
            f" {simulator.strategy.strategy_name} Weighted Strategy",
            "black",
        )

    def plot_buy_and_hold_unweighted_strategy(self, parameter: Parameter):
        portfolio = PortfolioUngewichtet(parameter.amount, parameter.anzahlAktien)
        strategy = BuyHoldStrategy()
        strategy.set_StockFetcher(self.stock_exchange)
        simulator = Simulator(self.stock_exchange, strategy, parameter, portfolio)
        simulator.simulate()
        self.updateplot(
            simulator,
            f" {simulator.strategy.strategy_name} Unweighted Strategy",
            "gray",
        )

    def plot_matplit_vor_update(self):
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

        self.ax.clear()

    def get_parameter(self):

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
        return parameter

    def plot_aktualisieren(self):
        # Beispiel: Plot je nach Auswahl
        # tickers = BASKETS["Nasdaq 100 Tech-Stocks"]
        self.plot_matplit_vor_update()
        basketStr = self.dropdown2.get()
        tickers = list(
            list(filter(lambda x: list(x.keys())[0] == basketStr, BASKETS))[0].values()
        )[0]
        parameter = self.get_parameter()

        stockexchange = FetchStock(
            tickers,
            parameter.start_date,
            parameter.end_date,
            YFinanceFetcher(),
        )
        self.stock_exchange = stockexchange
        data = stockexchange.fetch_data()
        data.to_csv()

        # self.plot_dispo_strategy(parameter)
        # self.plot_normal_strategy(parameter)
        self.plot_buy_and_hold_weighted_strategy(parameter)
        self.plot_buy_and_hold_unweighted_strategy(parameter)

        self.normalSimulator
        dd = {
            "config": str(parameter),
            "normal_metrics": (
                None if self.normalSimulator is None else self.normalSimulator.metrics
            ),
            "dispo_metrics": (
                None if self.dispoSimulator is None else self.dispoSimulator.metrics
            ),
            "buy_and_hold_metrics": self.buyHoldSimulator.metrics,
            "performance_diff": (
                "Ein atrument is None"
                if self.dispoSimulator is None or self.normalSimulator is None
                else calc_diff_disp_norm(
                    self.dispoSimulator.metrics["apy"],
                    self.normalSimulator.metrics["apy"],
                )
            ),
        }
        id = int(time.time())
        path = f"{date.today()}-{basketStr}-AA-{parameter.anzahlAktien}-DG-{parameter.dispoGrenze}-{id}"
        full_path = os.path.join(result_path, f"{path}.json")

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(dd, f, ensure_ascii=False, indent=4)

        # json.dump(dd, open(full_path, "w"))

        self.ax.legend()  # Legende nach dem Plotten der Linien aufrufen!
        plt.tight_layout()
        plt.xticks(rotation=45, ha="right")
        self.canvas.draw()

        plotPath = os.path.join(result_path, f"{path}.png")
        plt.savefig(
            plotPath, dpi=300, bbox_inches="tight", pad_inches=0.3
        )  # dpi=300 für hohe Qualität

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
