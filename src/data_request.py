import yfinance as yf

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
