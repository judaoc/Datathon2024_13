import json
import pandas as pd
import pandas_ta as ta
import yfinance as yf

from io import StringIO
from requests_html import HTMLSession
from yahoo_fin import stock_info as si

#converts the data to JSON format
def convertToJson(data):
    return json.dumps(data)

#returns the balance sheet in Dataframe from yfinance (ticker is the symbol, example: 'AAPL')
def getBalanceSheet(ticker):
    data = yf.Ticker(ticker)
    return data.balance_sheet

#returns the income statement in Dataframe from yfinance (ticker is the symbol, example: 'AAPL')
def getIncomeStatement(ticker):
    data = yf.Ticker(ticker)
    return data.financials

#returns the cash flow statement in Dataframe from yfinance (ticker is the symbol, example: 'AAPL')
def getCashFlowStatement(ticker):
    data = yf.Ticker(ticker)
    return data.cashflow

#returns the info in JSON from yfinance (ticker is the symbol, example: 'AAPL')
def getInfo(ticker):
    data = yf.Ticker(ticker)
    return convertToJson(data.info)

#returns the news of the company in JSON from yfinance (ticker is the symbol, example: 'AAPL')
def getNews(ticker):
    data = yf.Ticker(ticker)
    return convertToJson(data.news.to_json())

#write the financial report in a JSON file
def getFinancialReport(ticker):
    dataBalanceSheet = getBalanceSheet(ticker)
    dataIncomeStatement = getIncomeStatement(ticker)
    dataCashFlowStatement = getCashFlowStatement(ticker)

    for df in [dataBalanceSheet, dataIncomeStatement, dataCashFlowStatement]:
        df.columns = df.columns.astype(str)
        df.index = df.index.astype(str)

    financialReport = {
        "BalanceSheet": dataBalanceSheet.to_dict(),
        "IncomeStatement": dataIncomeStatement.to_dict(),
        "CashFlowStatement": dataCashFlowStatement.to_dict()
    }

    return financialReport

def getHistoricalData(ticker, period = '1y', interval = '1d'):
    data = yf.Ticker(ticker)
    return data.history(period=period, interval=interval)

def patched_raw_get_daily_info(url):
    session = HTMLSession()
    r = session.get(url)
    html_content = StringIO(r.html.html)
    tables = pd.read_html(html_content)
    df = tables[0].copy()
    
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

si._raw_get_daily_info = patched_raw_get_daily_info

def getTrendy():
    df = si.get_day_most_active()
    return df.head(8)

def getIndicators(dataframe):
    dataframe["RSI_14"] = ta.rsi(dataframe["Close"], length=14)
    dataframe["OBV"] = ta.obv(dataframe["Close"], dataframe["Volume"])
    macd = ta.macd(dataframe['Close'], fast=12, slow=26, signal=9)
    dataframe = pd.concat([dataframe, macd], axis=1)
    dataframe = pd.concat([dataframe, macd], axis=1)
    return dataframe

def getMACD(dataframe):
    macd = ta.macd(dataframe["Close"])
    return macd

def get_history(ticker_symbol, period="1y"):
    ticker = yf.Ticker(ticker_symbol)
    return ticker.history(period=period)

def get_rsi(ticker_symbol, period="1y", length=14):
    history = get_history(ticker_symbol, period)
    rsi = ta.rsi(history['Close'], length=length)
    return rsi

def get_macd(ticker_symbol, period="1y", short_period=12, long_period=26, signal_period=9):
    history = get_history(ticker_symbol, period)
    macd = ta.macd(history['Close'], fast=short_period, slow=long_period, signal=signal_period)
    return macd

def get_obv(ticker_symbol, period="1y"):
    history = get_history(ticker_symbol, period)
    obv = ta.obv(history['Close'], history['Volume'])
    return obv
