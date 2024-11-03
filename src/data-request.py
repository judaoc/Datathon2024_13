import yfinance as yf
import pandas as pd
import json
import pandas_ta as ta

#converts the data to JSON format
def convertToJson(data):
    return data.to_json()

#returns the balance sheet in JSON from yfinance (ticker is the symbol, example: 'AAPL')
def getBalanceSheet(ticker):
    data = yf.Ticker(ticker)
    return convertToJson(data.balance_sheet)

#returns the income statement in JSON from yfinance (ticker is the symbol, example: 'AAPL')
def getIncomeStatement(ticker):
    data = yf.Ticker(ticker)
    return convertToJson(data.financials)

#returns the cash flow statement in JSON from yfinance (ticker is the symbol, example: 'AAPL')
def getCashFlowStatement(ticker):
    data = yf.Ticker(ticker)
    return convertToJson(data.cashflow)

#returns the info in JSON from yfinance (ticker is the symbol, example: 'AAPL')
def getInfo(ticker):
    data = yf.Ticker(ticker)
    return data.info

#returns the news of the company in JSON from yfinance (ticker is the symbol, example: 'AAPL')
def getNews(ticker):
    data = yf.Ticker(ticker)
    return data.news

#write the financial report in a JSON file
def writeFinancialReport(dataBalanceSheet, dataIncomeStatement, dataCashFlowStatement,ticker):
    financialReport_json = {
        "BalanceSheet": dataBalanceSheet,
        "IncomeStatement": dataIncomeStatement,
        "CashFlowStatement": dataCashFlowStatement
    }
    with open(ticker+'_AnnualFinancialReport.json', 'w') as file:
        json.dump(financialReport_json, file, indent=4)

#returns the historical data in Dataframe from yfinance (ticker is the symbol, example: 'AAPL', period is the time period, example: '1y', interval is the time interval, example: '1d')
def getHistoricalData(ticker, period = '1y', interval = '1d'):
    data = yf.Ticker(ticker)
    return data.history(period=period, interval=interval)

#indicators (RSI, MACD, OBV)
def getIndicators(dataframe):
    dataframe["RSI_14"] = ta.rsi(dataframe["Close"], length=14)
    dataframe["OBV"] = ta.obv(dataframe["Close"], dataframe["Volume"])
    # macd = ta.trend.MACD(dataframe['Close'], fast=12, slow=26, signal=9)
    # macd = ta.macd(dataframe["Close"])
    macd = ta.macd(dataframe['Close'], fast=12, slow=26, signal=9)
    dataframe = pd.concat([dataframe, macd], axis=1)
    #print(macd)
    dataframe = pd.concat([dataframe, macd], axis=1)
    return dataframe
def getMACD(dataframe):
    macd = ta.macd(dataframe["Close"])
    return macd
#example of how to use the functions
# symbol = 'AAPL'
# apple = yf.Ticker(symbol)
# news = getNews(symbol)
# info = getInfo(symbol)
# with open('info.json', 'w') as file:
#     json.dump(news, file, indent=4)

dataframe = getHistoricalData('AAPL', period='1y', interval='1d')
#dataframe0 = getMACD(dataframe)
dataframe1 = getIndicators(dataframe)

print(dataframe1.columns)