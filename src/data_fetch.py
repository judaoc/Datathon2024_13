import yfinance as yf
import pandas as pd
import json
import pandas_ta as ta

#converts the data to JSON format
def convertToJson(data):
    return json.dumps(data)

#returns the balance sheet in JSON from yfinance (ticker is the symbol, example: 'AAPL')
def getBalanceSheet(ticker):
    data = yf.Ticker(ticker)
    return (data.balance_sheet).to_json()

#returns the income statement in JSON from yfinance (ticker is the symbol, example: 'AAPL')
def getIncomeStatement(ticker):
    data = yf.Ticker(ticker)
    return (data.financials).to_json()

#returns the cash flow statement in JSON from yfinance (ticker is the symbol, example: 'AAPL')
def getCashFlowStatement(ticker):
    data = yf.Ticker(ticker)
    return (data.cashflow).to_json()

#returns the info in JSON from yfinance (ticker is the symbol, example: 'AAPL')
def getInfo(ticker):
    data = yf.Ticker(ticker)
    return convertToJson(data.info)

#returns the news of the company in JSON from yfinance (ticker is the symbol, example: 'AAPL')
def getNews(ticker):
    data = yf.Ticker(ticker)
    return convertToJson(data.news.to_json())

#write the financial report in a JSON file
def writeFinancialReport(ticker):
    return {
        "BalanceSheet": getBalanceSheet(ticker),
        "IncomeStatement": getIncomeStatement(ticker),
        "CashFlowStatement": getCashFlowStatement(ticker)
    }

#returns the historical data in Dataframe from yfinance (ticker is the symbol, example: 'AAPL', period is the time period, example: '1y', interval is the time interval, example: '1d')
def getHistoricalData(ticker, period = '1y', interval = '1d'):
    data = yf.Ticker(ticker)
    return data.history(period=period, interval=interval)

#indicators (RSI, MACD, OBV)
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
