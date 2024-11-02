import yfinance as yf
import pandas as pd
import json

#import the balance sheet in JSON (ticker is the symbol, example: 'AAPL')
def getBalanceSheet(ticker):
    data = yf.Ticker(ticker)
    return convertToJson(data.balance_sheet)

#import the income statement in JSON (ticker is the symbol, example: 'AAPL')
def getIncomeStatement(ticker):
    data = yf.Ticker(ticker)
    return convertToJson(data.financials)

#import the cash flow statement in JSON (ticker is the symbol, example: 'AAPL')
def getCashFlowStatement(ticker):
    data = yf.Ticker(ticker)
    return convertToJson(data.cashflow)

#import the info in JSON (ticker is the symbol, example: 'AAPL')
def getInfo(ticker):
    data = yf.Ticker(ticker)
    return convertToJson(data.info)

def convertToJson(data):
    return data.to_json()

def writeFinancialReport(dataBalanceSheet, dataIncomeStatement, dataCashFlowStatement,ticker):
    financialReport_json = {
        "BalanceSheet": dataBalanceSheet,
        "IncomeStatement": dataIncomeStatement,
        "CashFlowStatement": dataCashFlowStatement
    }
    with open(ticker+'_AnnualFinancialReport.json', 'w') as file:
        json.dump(financialReport_json, file, indent=4)

#example of how to use the functions
symbol = 'AAPL'
balanceSheet=getBalanceSheet(symbol)
#balanceSheet_json = balanceSheet.to_json()
#with open('balanceSheet.json', 'w') as file:
#    pass
#with open('balanceSheet.json', 'w') as file:
#    json.dump(balanceSheet_json, file, indent=4)

incomeStatement=getIncomeStatement(symbol)
#print(incomeStatement.head(100))

cashFlowStatement=getCashFlowStatement(symbol)
#print(cashFlowStatement.head(100))

#get the news of a company (ticker is the symbol, example: 'AAPL')
#apple = yf.Ticker('AAPL')
#print(apple.news)

#testing creating an annual financial report
#dataBalanceSheet = convertToJson(balanceSheet_pd)
#dataIncomeStatement = convertToJson(incomeStatement_pd)
#dataCashFlowStatement = convertToJson(cashFlowStatement_pd)
writeFinancialReport(balanceSheet, incomeStatement, cashFlowStatement,symbol)
