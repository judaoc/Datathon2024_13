from requests_html import HTMLSession
import yfinance as yf
from yahoo_fin import stock_info as si
import json
import pandas as pd
from io import StringIO
import os

def getBalanceSheet(ticker):
    data = yf.Ticker(ticker)
    return data.balance_sheet

def getIncomeStatement(ticker):
    data = yf.Ticker(ticker)
    return data.financials

def getCashFlowStatement(ticker):
    data = yf.Ticker(ticker)
    return data.cashflow

def getFinancialReport(ticker):
    dataBalanceSheet = getBalanceSheet(ticker)
    dataIncomeStatement = getIncomeStatement(ticker)
    dataCashFlowStatement = getCashFlowStatement(ticker)

    # Convertir les colonnes et les index en chaînes de caractères
    for df in [dataBalanceSheet, dataIncomeStatement, dataCashFlowStatement]:
        df.columns = df.columns.astype(str)
        df.index = df.index.astype(str)

    financialReport = {
        "BalanceSheet": dataBalanceSheet.to_dict(),
        "IncomeStatement": dataIncomeStatement.to_dict(),
        "CashFlowStatement": dataCashFlowStatement.to_dict()
    }
    return financialReport

def patched_raw_get_daily_info(url):
    session = HTMLSession()
    r = session.get(url)
    html_content = StringIO(r.html.html)
    tables = pd.read_html(html_content)
    df = tables[0].copy()
    
    # List of columns that need to be dropped
    columns_to_drop = [
        '52 Week Range',
        'PE Ratio (TTM)',
        'Volume',
        'Avg Vol (3 month)',
        'Name',
        'Change',
        'Avg Vol (3M)', 
        'Market Cap', 
        'P/E Ratio (TTM)', 
        '52 Wk Change %', 
        '52 Wk Range',
        'Unnamed: 2',
        'Change %'
    ]
    
    for col in columns_to_drop:
        if col in df.columns:
            df = df.drop(columns=[col], errors='ignore')
    df = df.reset_index(drop=True)
    session.close()
    return df

# Replace the original function
si._raw_get_daily_info = patched_raw_get_daily_info

def getTrendy():
    df = si.get_day_most_active()
    return df.head(10)