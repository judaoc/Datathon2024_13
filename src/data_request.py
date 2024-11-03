import yfinance as yf
import json

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
