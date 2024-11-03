from requests_html import HTMLSession
import yfinance as yf
from yahoo_fin import stock_info as si
import json
import pandas as pd
from io import StringIO

def convert_to_json(data):
    return data.to_json()

def get_balance_sheet(ticker):
    data = yf.Ticker(ticker)
    return convert_to_json(data.balance_sheet)

def get_income_statement(ticker):
    data = yf.Ticker(ticker)
    return convert_to_json(data.financials)

def get_cash_flow_statement(ticker):
    data = yf.Ticker(ticker)
    return convert_to_json(data.cashflow)

def write_financial_report(ticker):
    financial_report_json = {
        "BalanceSheet": get_balance_sheet(ticker),
        "IncomeStatement": get_income_statement(ticker),
        "CashFlowStatement": get_cash_flow_statement(ticker)
    }
    with open(f'{ticker}_AnnualFinancialReport.json', 'w') as file:
        json.dump(financial_report_json, file, indent=4)

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

def get_trendy():
    df = si.get_day_most_active()
    return df.head(10)