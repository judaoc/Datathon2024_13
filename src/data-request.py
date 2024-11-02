import yfinance as yf
import pandas as pd
import json

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

#example of how to use the functions
# symbol = 'AAPL'
# apple = yf.Ticker(symbol)
# news = getNews(symbol)
# info = getInfo(symbol)
# with open('info.json', 'w') as file:
#     json.dump(news, file, indent=4)
