from config.baskets.DAX40 import DAX40
from config.baskets.EUROPE_STOXX_600 import EUROPE_STOX_600
from config.baskets.NASDAQ100 import NADAQ
from config.baskets.nikkei import NIKKEI
from config.baskets.SP500 import SP500

BASKETS = [
    {"NASDAQ": NADAQ},
    {"DAX": DAX40},

    {"NIKKEY": NIKKEI},
    {"SP500": SP500},
    {"EURO_STOX": EUROPE_STOX_600},
]
