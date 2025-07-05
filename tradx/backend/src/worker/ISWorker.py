import json
import pandas as pd
import time
from tradx.backend.src.worker.db.FInDBWorker import FInDBWorker as FINDB
from tradx.backend.src.worker.db.StockDBWorker import StockDBWorker as StockDB
import yfinance as yf
from multiprocessing import Queue 

STOCK_DB = StockDB(Queue())
ISINS = STOCK_DB.get_isins()

def get_period(columns: pd.DatetimeIndex, query: pd.Timestamp) -> dict:
    """
    Ermittelt die Periode (z.B. 'Q4 FY2024') auf Basis eines Spalten-DatetimeIndex.

    Args:
        columns (pd.DatetimeIndex): Die Datumsangaben aus income_stmt.columns.
        query (str): 'annual' oder 'quarterly'

    Returns:
        dict: {
            'fy_end_date': datetime,
            'fy_year': int,
            'quarter': str,
            'label': str  # z.B. 'Q4 FY2024'
        }
    """
    if columns.empty:
        return {'fy_end_date': None, 'fy_year': None, 'quarter': None, 'label': None}

    latest = columns.max()
    fy_year = query.year
    quarter = (query.month - 1) // 3 + 1
    return {
        'fy_end_date': latest,
        'fy_year': fy_year,
        'quarter': f"Q{quarter}",
        'label': f"Q{quarter} FY{fy_year}"
    }


def process_isin(isin:str, fin_db:FINDB):
    ticker = yf.Ticker(isin)
    yearly_stmts = ticker.income_stmt
    dd = {}
    dd["isin"] = isin
    dd["ticker"] = StockDB.get_ticker(isin)
    currency  = StockDB.get_currency(isin=isin)
    yearly_cols = yearly_stmts.columns
    for fy in yearly_stmts.columns:
        col = yearly_stmts[fy]
        dd["period"] = f"FY{fy.year}"
        dd["fy_end_date"] = int(fy.timestamp())
        
        dd["totalRevenue"] = col.loc["Total Revenue"]
        dd["operatingRevenue"] = col.loc["Operating Revenue"]
        dd["costOfRevenue"] = col.loc["Operating Revenue"]
        dd["grossProfit"] = col.loc["Gross Profit"]
        dd["researchAndDevelopment"] 
        dd["sellingGeneralAndAdmin"] INTEGER,
        dd["operatingExpense"] INTEGER,
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
    
        rssdb.queue.put({
            "type": "insert_rss",
            "payload": dd
        })
    return max_id


def main(debug=False):
    q = Queue()
    fin_db = FINDB(q)
    fin_db.start()

    for isin in ISINS:
        time.sleep(1)
        new_max =  process_isin()
        
    

if __name__ == "__main__":
    main()





