from strategies.GrowthStratregy import GrowthStrategy
from strategies.high_valatility_strategy import HighValatilityStrategy
from strategies.KGVStratregy import KGVStrategy
from strategies.low_valatility_strategy import LowValatilityStrategy
from strategies.momentum_strategy import MomentumStrategy
from strategies.movingAverageCrossoverStrategy import MovingAverageCrossoverStrategy
from strategies.random_strategy import RandomStrategy
from strategies.reversion_strategy import ReversionStrategy
from strategies.rsiStrategy import RSIStrategy

strategies = [
    {"name": "random", "strategy": RandomStrategy()},
    {
        "name": "momentum",
        "strategy": MomentumStrategy(),
    },
    {"name": "low_volatility", "strategy": LowValatilityStrategy()},
    {"name": "high_volatility", "strategy": HighValatilityStrategy()},
    {"name": "mean_reversion", "strategy": ReversionStrategy()},
    {"name": "moving_average_crossover", "strategy": MovingAverageCrossoverStrategy()},
    {"name": "RSI", "strategy": RSIStrategy()},
  
    {
        "name": "growth",
        "strategy": GrowthStrategy(),
    },
    {"name": "kgv", "strategy": KGVStrategy()},
]

FREQUENCY = [
    {"id": "once", "name": "1 mal am Tag"},
    {"id": "twice", "name": "1 mal alle 2 Tag"},
    {"id": "once_week", "name": "1 mal in der  Woche"},
    {"id": "once_month", "name": "Alle 4 Wochen"},
    {"id": "once_6_month", "name": "Alle 6 Monate"},
]

# --- 1. Große Baskets (repräsentative Auswahl, Stand 2024) ---
BASKETS = {
    "Nasdaq 100 Tech-Stocks": [
        "AAPL",
        "MSFT",
        "GOOGL",
        "GOOG",
        "NVDA",
        "META",
        "AVGO",
        "TSLA",
        "ADBE",
        "CSCO",
        "AMD",
        "INTC",
        "AMZN",
        "QCOM",
        "TXN",
        "AMAT",
        "ASML",
        "LRCX",
        "ADI",
        "KLAC",
        "SNPS",
        "CRWD",
        "PANW",
        "CDNS",
        "MRVL",
        "MCHP",
        "ORCL",
        "INTU",
        "WDAY",
        "TEAM",
        "ZM",
    ],
    "S&P 500 Large Caps": [
        "AAPL",
        "MSFT",
        "AMZN",
        "GOOGL",
        "GOOG",
        "META",
        "BRK-B",
        "NVDA",
        "TSLA",
        "UNH",
        "JPM",
        "V",
        "MA",
        "HD",
        "PG",
        "LLY",
        "XOM",
        "CVX",
        "ABBV",
        "AVGO",
        "COST",
        "PEP",
        "KO",
        "MRK",
        "WMT",
        "BAC",
        "DIS",
        "MCD",
        "ADBE",
        "CMCSA",
    ],
    "MSCI World Top 50": [
        "AAPL",
        "MSFT",
        "AMZN",
        "NVDA",
        "GOOGL",
        "GOOG",
        "META",
        "TSLA",
        "UNH",
        "JPM",
        "V",
        "MA",
        "HD",
        "PG",
        "LLY",
        "XOM",
        "CVX",
        "ABBV",
        "AVGO",
        "COST",
        "PEP",
        "KO",
        "MRK",
        "WMT",
        "BAC",
        "DIS",
        "MCD",
        "ADBE",
        "CMCSA",
        "BHP",
        "TM",
        "SHEL",
        "TMO",
        "NVO",
        "SAP",
        "LIN",
        "ORCL",
        "ASML",
        "SNY",
        "AZN",
        "RDS-A",
        "RDS-B",
        "BAYRY",
        "UL",
        "NESN",
        "DHR",
        "HON",
        "AMGN",
        "TXN",
    ],
    "DAX 40": [
        "ADS",
        "AIR",
        "ALV",
        "BAS",
        "BAYN",
        "BEI",
        "BMW",
        "BNR",
        "CON",
        "1COV",
        "DB1",
        "DBK",
        "DHL",
        "DTE",
        "ENR",
        "EOAN",
        "FME",
        "FRE",
        "HEI",
        "HEN3",
        "IFX",
        "LIN",
        "MRK",
        "MTX",
        "MUV2",
        "PAH3",
        "PUM",
        "QIA",
        "RWE",
        "SAP",
        "SIE",
        "SHL",
        "SY1",
        "VOW3",
        "VNA",
        "ZAL",
    ],
    "EU Tech Leaders": [
        "ASML",
        "SAP",
        "ADYEN",
        "STM",
        "NOKIA",
        "INFN",
        "AMS",
        "SIE",
        "IFX",
        "NEM",
        "CAP",
        "SOP",
        "ATOS",
        "WDI",
        "LOGN",
        "ROG",
        "DSY",
        "SU",
        "OR",
        "AIR",
        "ALV",
        "BAS",
        "BAYN",
        "BEI",
        "BMW",
        "BNR",
        "CON",
    ],
    "Value Stocks (US)": [
        "WFC",
        "C",
        "BAC",
        "CVX",
        "XOM",
        "PFE",
        "VZ",
        "T",
        "GM",
        "F",
        "INTC",
        "CSCO",
        "IBM",
        "MMM",
        "GE",
        "WBA",
        "KHC",
        "MO",
        "TFC",
        "USB",
        "MET",
        "PRU",
        "AIG",
        "ALL",
        "KR",
        "GIS",
        "K",
        "CPB",
        "HSY",
        "SJM",
    ],
    "High Dividend Stocks (Global)": [
        "MO",
        "PM",
        "T",
        "VZ",
        "IBM",
        "XOM",
        "CVX",
        "BHP",
        "RIO",
        "SHEL",
        "ENB",
        "PFE",
        "GSK",
        "UL",
        "NGG",
        "TOT",
        "BCE",
        "BTI",
        "EPD",
        "MPLX",
        "OKE",
        "PSX",
        "SNP",
        "SU",
        "TEF",
        "VOD",
        "WMB",
        "ZIM",
        "FRO",
        "E",
        "EQNR",
    ],
    "Emerging Markets Top 30": [
        "TSM",
        "BABA",
        "TCEHY",
        "JD",
        "PDD",
        "INFY",
        "HDB",
        "VALE",
        "PBR",
        "ITUB",
        "MELI",
        "YPF",
        "GGB",
        "SBER",
        "GAZP",
        "LUKOY",
        "NORN",
        "YNDX",
        "MTL",
        "MBT",
        "NIO",
        "XPEV",
        "LI",
        "BYD",
        "JD",
        "BIDU",
        "NTES",
        "CTRP",
        "ZTO",
        "EDU",
    ],
    "Green & ESG Stocks": [
        "ORSTED.CO",
        "VWS.CO",
        "ENPH",
        "SEDG",
        "PLUG",
        "TSLA",
        "NIO",
        "BYD",
        "FSLR",
        "NEE",
        "ED",
        "REGI",
        "RUN",
        "SPWR",
        "VWDRY",
        "SGRE.MC",
        "ALB",
        "LIN",
        "NXPI",
        "AEP",
        "AES",
        "AY",
        "CWEN",
        "BE",
        "BLDP",
        "CVA",
        "DNNGY",
        "EVRG",
        "FANUY",
        "HASI",
    ],
    "Crypto-Exposed Equities": [
        "COIN",
        "MSTR",
        "RIOT",
        "MARA",
        "HUT",
        "BTBT",
        "BITF",
        "CAN",
        "SI",
        "SBNY",
        "OSTK",
        "NVDA",
        "TSLA",
        "PYPL",
        "SQ",
        "GLXY.TO",
        "CLSK",
        "SDIG",
        "HIVE",
        "DGHI",
        "BITF",
        "BTCS",
        "BKKT",
        "CIFR",
        "GREE",
        "HUT",
        "IREN",
        "WULF",
        "ARBK",
        "BRPHF",
    ],
}
