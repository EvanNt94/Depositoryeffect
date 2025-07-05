from pathlib import Path
import sqlite3

DB_DIR = Path.home() / "db" / "tradx"
DB_DIR.mkdir(parents=True, exist_ok=True)

# stock.db for stock table
STOCK_DB_PATH = DB_DIR / "stock.db"
conn_stock = sqlite3.connect(STOCK_DB_PATH)
cursor_stock = conn_stock.cursor()

cursor_stock.execute("""
CREATE TABLE IF NOT EXISTS stock (
    ticker TEXT,
    isin TEXT PRIMARY KEY,
    name TEXT,
    longName TEXT,
    website TEXT,
    industryKey TEXT,
    sectorKey TEXT,
    summary TEXT,
    employees INTEGER,
    irWebsite TEXT,
    dividend FLOAT,
    fiveYearAvgDividendYield FLOAT,
    beta FLOAT, 
    street TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    country TEXT,
    currency TEXT,
    region TEXT,
    ipo INTEGER,
    last_updated INTEGER
)
""")

conn_stock.commit()
conn_stock.close()

# dividends.db for dividend table
DIVIDENDS_DB_PATH = DB_DIR / "dividends.db"
conn_dividends = sqlite3.connect(DIVIDENDS_DB_PATH)
cursor_dividends = conn_dividends.cursor()

cursor_dividends.execute("""
CREATE TABLE IF NOT EXISTS dividend (
    isin TEXT PRIMARY KEY,
    price REAL,
    dividend REAL,
    epoch INTEGER,
    annualYield REAL,
    last_updated INTEGER
)
""")

conn_dividends.commit()
conn_dividends.close()

# financials.db for fundamentals, income_statement, estimates tables
FINANCIALS_DB_PATH = DB_DIR / "financials.db"
conn_financials = sqlite3.connect(FINANCIALS_DB_PATH)
cursor_financials = conn_financials.cursor()

cursor_financials.execute("""
CREATE TABLE IF NOT EXISTS fundamentals (
    isin TEXT PRIMARY KEY,
    ticker TEXT,
    trailingPE REAL,
    forwardPE REAL,
    marketCap INTEGER,
    enterpriseValue INTEGER,
    profitMargins REAL,
    floatShares INTEGER,
    sharesOutstanding INTEGER,
    sharesShort INTEGER,
    sharesShortPriorMonth INTEGER,
    sharesShortPreviousMonthDate INTEGER,
    dateShortInterest INTEGER,
    sharesPercentSharesOut REAL,
    heldPercentInsiders REAL,
    heldPercentInstitutions REAL,
    shortRatio REAL,
    shortPercentOfFloat REAL,
    impliedSharesOutstanding INTEGER,
    bookValue REAL,
    priceToBook REAL,
    earningsQuarterlyGrowth REAL,
    netIncomeToCommon INTEGER,
    trailingEps REAL,
    forwardEps REAL,
    enterpriseToRevenue REAL,
    enterpriseToEbitda REAL,
    totalCash INTEGER,
    totalCashPerShare REAL,
    ebitda INTEGER,
    ebitdaNormalized INTEGER, 
    totalDebt INTEGER,
    quickRatio REAL,
    currentRatio REAL,
    totalRevenue INTEGER,
    revenuePerShare REAL,
    debtToEquity REAL,
    returnOnAssets REAL,
    grossProfits INTEGER,
    freeCashflow INTEGER,
    operatingCashflow INTEGER,
    earningsGrowth REAL,
    revenueGrowth REAL,
    grossMargins REAL,
    ebitdaMargins REAL,
    operatingMargins REAL,
    taxRate REAL,
    epsTrailingTwelveMonths REAL,
    epsForward REAL,
    epsCurrentYear REAL,
    priceEpsCurrentYear REAL,
    trailingPegRatio REAL,
    returnOnEquity REAL,
    last_updated INTEGER
)
""")

cursor_financials.execute("""
CREATE TABLE IF NOT EXISTS income_statement (
    isin TEXT,
    ticker TEXT,
    period TEXT,
    fy_end_date INTEGER,
    currency TEXT,
    totalRevenue INTEGER,
    operatingRevenue INTEGER,
    costOfRevenue INTEGER,
    grossProfit INTEGER,
    researchAndDevelopment INTEGER,
    sellingGeneralAndAdmin INTEGER,
    operatingExpense INTEGER,
    otherNonOperatingIncomeExpense INTEGER,
    totalExpenses INTEGER,
    operatingIncome INTEGER,
    totalOperatingIncomeAsReported INTEGER,
    interestIncome INTEGER,
    interestExpense INTEGER,
    netInterestIncome INTEGER,
    otherIncomeExpense INTEGER,
    pretaxIncome INTEGER,
    taxProvision INTEGER,
    taxEffectOfUnusualItems INTEGER,
    netIncome INTEGER,
    netIncomeFromContinuingAndDiscontinued INTEGER,
    normalizedIncome INTEGER,
    interestIncomeNonOperating INTEGER,
    netNonOperatingInterestIncomeExpense INTEGER,
    normalizedEBITDA INTEGER,
    ebit INTEGER,
    interestExpenseNonOperating INTEGER,
    ebitda INTEGER,
    reconciledDeprecation INTEGER,
    reconciledCostOfRevenue INTEGER,
    dilutedNetIncomeToCommon INTEGER,
    dilutedEPS REAL,
    basicEPS REAL,
    dilutedShares INTEGER,
    basicShares INTEGER,
    netIncomeCommonStockholders INTEGER, 
    netIncomeIncludingNoncontrolling INTEGER,
    netIncomeFromContinuingOperations INTEGER,
    last_updated INTEGER,
    PRIMARY KEY (isin, period)
)
""")

cursor_financials.execute("""
CREATE TABLE IF NOT EXISTS estimates (
    isin TEXT,
    ticker TEXT,
    targetHighPrice REAL,
    targetLowPrice REAL,
    targetMeanPrice REAL,
    targetMedianPrice REAL,
    recommendationMean REAL,
    numberOfAnalystOpinions INTEGER,
    averageAnalystRating TEXT,
    last_updated INTEGER,
    PRIMARY KEY (isin)
)
""")

conn_financials.commit()
conn_financials.close()

# price.db for daily_price and intraday_price_15min tables
PRICE_DB_PATH = DB_DIR / "price.db"
conn_price = sqlite3.connect(PRICE_DB_PATH)
cursor_price = conn_price.cursor()

cursor_price.execute("""
CREATE TABLE IF NOT EXISTS daily_price (
    isin TEXT,
    date INTEGER,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    last_updated INTEGER,
    PRIMARY KEY (isin, date)
)
""")

cursor_price.execute("""
CREATE TABLE IF NOT EXISTS intraday_price_15min (
    isin TEXT,
    ticker TEXT,
    timestamp INTEGER,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER,
    last_updated INTEGER,
    PRIMARY KEY (isin, timestamp)
)
""")

conn_price.commit()
conn_price.close()

# leadership.db for leadership, risk_scores, risk_events tables
LEADERSHIP_DB_PATH = DB_DIR / "leadership.db"
conn_leadership = sqlite3.connect(LEADERSHIP_DB_PATH)
cursor_leadership = conn_leadership.cursor()

cursor_leadership.execute("""
CREATE TABLE IF NOT EXISTS leadership (
    isin TEXT,
    ticker TEXT,
    name TEXT,
    title TEXT,
    age INTEGER,
    yearBorn INTEGER,
    fiscalYear INTEGER,
    totalPay INTEGER,
    exercisedValue INTEGER,
    unexercisedValue INTEGER,
    maxAge INTEGER,
    last_updated INTEGER,
    PRIMARY KEY (isin, name)
)
""")

cursor_leadership.execute("""
CREATE TABLE IF NOT EXISTS risk_scores (
    isin TEXT,
    ticker TEXT,
    source TEXT,
    date INTEGER,
    category TEXT,
    value REAL,
    last_updated INTEGER,
    PRIMARY KEY (isin, source, date, category)
)
""")

cursor_leadership.execute("""
CREATE TABLE IF NOT EXISTS risk_events (
    isin TEXT,
    ticker TEXT,
    date INTEGER,
    description TEXT,
    severity INTEGER,
    source TEXT,
    last_updated INTEGER,
    PRIMARY KEY (isin, date, source)
)
""")

conn_leadership.commit()
conn_leadership.close()
