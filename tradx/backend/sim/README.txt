# Simulation Framework für Derivate und Stochastische Prozesse

Dieses Modul erlaubt die Monte-Carlo-Simulation stochastischer Prozesse (z. B. Heston, GBM, CIR) und die darauf basierende Bewertung von Derivaten (europäische, exotische Optionen). Es ist modular aufgebaut und erlaubt einfache Erweiterung um neue Prozesse, Instrumente und Visualisierungen.

---

## 📁 Verzeichnisstruktur (Auszug)

/Users/a2/code/fin/trade/tradx/backend/sim
├── configs
├── derivative
│   ├── base.py
│   ├── european.py
│   ├── exotic.py
│   ├── info.txt
│   └── Pricer.py
├── MeasureChanger.py
├── stochastic_process
    ...
│   └── StochasticProcess.py
└── visual
    ├── HeatmapPlotter.py
    ├── PathPlotter.py
    └── SurfacePlotter.py

---

## 🧮 Beispiel 1: Preis- und Volatilitätspfad (Heston)

```python
from stochastic_process.HestonModel import HestonModel
from visual.PathPlotter import PathPlotter

heston = HestonModel(mu=0.05, kappa=1.5, theta=0.04, sigma=0.3, rho=-0.7, v0=0.04, s0=100)
S, v = heston.simulate_path(T=1.0, N=252, M=10)

PathPlotter.plot_price_paths(S)
PathPlotter.plot_vol_paths(v)

```

## 💰 Beispiel 2: Optionsbewertung
```python
from derivative.european import EuropeanCall
from derivative.Pricer import MonteCarloPricer

option = EuropeanCall(K=100, T=1.0)
pricer = MonteCarloPricer(option=option, model=heston)

price = pricer.price(M=10000, N=252)
print(f"Monte-Carlo Preis: {price:.2f}")
```

## 📊 Beispiel 3: Oberflächen-Plot
```python
from visual.SurfacePlotter import plot_surface
import numpy as np

X, Y = np.meshgrid(np.linspace(80, 120, 10), np.linspace(0.1, 2.0, 10))
Z = np.random.rand(10, 10)  # z. B. IV-Werte
plot_surface(X, Y, Z, title="IV-Surface", xlabel="Strike", ylabel="Maturity")
```

## 🧩 Eigene Modelle & Erweiterungen

- Neue stochastische Prozesse: Erben von `StochasticProcess` und implementieren `simulate_path(...)`
- Eigene Optionen: Leiten sich von `BaseOption` ab und definieren `payoff(...)`
- Der `MonteCarloPricer` kann jede dieser Klassen bewerten – auch mit exotischer Struktur
- Neue Visualisierungen lassen sich durch weitere Module im `visual/`-Ordner ergänzen


## 🔧 Technische Hinweise
- `simulate_path(...)` gibt ein Array der Form `(M, N)` zurück (M Pfade, N Zeitschritte)
- Pfade enthalten Assetpreise oder Volatilitätsentwicklungen je nach Modell
- Fallback-Mechanismen für numerisch instabile Simulationen sind in Planung