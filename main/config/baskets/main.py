from config.baskets.DAX40 import DAX40
from config.baskets.EUROPE_STOXX_600 import EURO600
from config.baskets.NASDAQ100 import NADAQ
from config.baskets.nikkei import nikkei225
from config.baskets.SP500 import SP500

BASKETS = [
    {"NASDAQ": NADAQ},
    {"DAX": DAX40},
    {"EURO_STOX": EURO600},
    {"NIKKEY": nikkei225},
    {"SP500": SP500},
]
