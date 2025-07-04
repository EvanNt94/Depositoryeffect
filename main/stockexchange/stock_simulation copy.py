import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class StockSimulator:
    def __init__(self, symbol, start_date, end_date, initial_capital=10000):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = []
        self.trades = []
        
    def fetch_data(self):
        """Lädt historische Aktiendaten"""
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
        return self.data
    
    def simulate(self):
        """Führt die Simulation durch"""
        if not hasattr(self, 'data'):
            self.fetch_data()
            
        current_position = None
        completed_trades = []  # Liste für abgeschlossene Trades
        
        for date, row in self.data.iterrows():
            close_price = float(row['Close'])  # Konvertiere zu float
            
            if current_position is None:  # Keine Position
                if self.capital >= close_price:  # Genug Kapital zum Kaufen
                    shares = 1  # Kaufen einer Aktie
                    cost = shares * close_price
                    self.capital -= cost
                    current_position = {
                        'shares': shares,
                        'entry_price': close_price,
                        'entry_date': date,
                        'buy_trade': {
                            'date': date,
                            'type': 'buy',
                            'price': close_price,
                            'shares': shares
                        }
                    }
            
            else:  # Position vorhanden
                # Berechne Gewinn/Verlust
                profit = (close_price - current_position['entry_price']) * current_position['shares']
                
                # Wenn Gewinn, dann verkaufen
                if profit > 0:
                    self.capital += close_price * current_position['shares']
                    sell_trade = {
                        'date': date,
                        'type': 'sell',
                        'price': close_price,
                        'shares': current_position['shares'],
                        'profit': profit
                    }
                    # Füge den kompletten Trade (Kauf und Verkauf) zur Liste hinzu
                    completed_trades.append({
                        'buy': current_position['buy_trade'],
                        'sell': sell_trade,
                        'profit': profit
                    })
                    current_position = None
        
        self.trades = completed_trades
        return completed_trades
    
    def plot_results(self):
        """Visualisiert die Ergebnisse"""
        if not self.trades:
            print("Keine Trades vorhanden")
            return
            
        # Erstelle DataFrame aus Trades
        trades_df = pd.DataFrame([{
            'date': trade['sell']['date'],
            'profit': trade['profit']
        } for trade in self.trades])
        
        # Berechne kumulativen Gewinn
        trades_df['cumulative_profit'] = trades_df['profit'].cumsum()
        
        # Plotte
        plt.figure(figsize=(12, 6))
        plt.plot(trades_df['date'], trades_df['cumulative_profit'])
        plt.title(f'Kumulativer Gewinn für {self.symbol}')
        plt.xlabel('Datum')
        plt.ylabel('Gewinn in USD')
        plt.grid(True)
        plt.show()

# Beispiel Verwendung
if __name__ == "__main__":
    # Beispiel mit Apple Aktien
    simulator = StockSimulator(
        symbol="AAPL",
        start_date="2023-01-01",
        end_date="2024-01-01",
        initial_capital=10000
    )
    
    trades = simulator.simulate()
    simulator.plot_results()
    
    # Ausgabe der Ergebnisse
    print(f"\nSimulationsergebnisse für {simulator.symbol}:")
    print(f"Anfangskapital: ${simulator.initial_capital:,.2f}")
    
    # Berechne den tatsächlichen Gewinn nur aus abgeschlossenen Trades
    total_profit = sum(trade['profit'] for trade in trades)
    final_capital = simulator.initial_capital + total_profit
    
    print(f"Endkapital (nur abgeschlossene Trades): ${final_capital:,.2f}")
    print(f"Gesamtgewinn aus abgeschlossenen Trades: ${total_profit:,.2f}")
    print(f"Anzahl der abgeschlossenen Trades: {len(trades)}")
    
    # Detaillierte Analyse der Trades
    if trades:
        avg_profit = total_profit / len(trades)
        print(f"Durchschnittlicher Gewinn pro Trade: ${avg_profit:,.2f}") 


def __main__():
    simulator = StockSimulator(
        symbol="AAPL",
        start_date="2023-01-01",
        end_date="2024-01-01",
        initial_capital=10000
    )
    trades = simulator.simulate()
    simulator.plot_results()