from requests_html import HTMLSession
import yfinance as yf
from yahoo_fin import stock_info as si
import json
from json_claude import analyzeArticles
from datetime import datetime, timedelta, timezone
import pandas as pd
from io import StringIO
import requests

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
    return df.head(8)

def getNews(api_key):
    url = f"https://newsapi.org/v2/everything?q=finance&sortBy=publishedAt&language=en&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        articles = response.json().get('articles', [])[:5]
        return [(article['title'], article['url']) for article in articles]
    else:
        print("error:", response.status_code)
        return []
    
def getSpecificNews(api_key, symbol):
    # Récupérer des articles triés par pertinence
    url = f"https://newsapi.org/v2/everything?q={symbol}&sortBy=relevancy&language=en&pageSize=100&apiKey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        articles = response.json().get('articles', [])

        recent_articles = []
        now_utc = datetime.now(timezone.utc)
        for article in articles:
            published_date = datetime.fromisoformat(article['publishedAt'].replace('Z', '+00:00'))
            if published_date >= now_utc - timedelta(days=3):
                recent_articles.append((article['title'], article['url']))
        recent_articles_json = json.dumps(recent_articles, indent=4)
        best_articles_indices = analyzeArticles(recent_articles_json, symbol)
        best_recent_articles = [recent_articles[int(i)] for i in best_articles_indices if int(i) < len(recent_articles)]
        return best_recent_articles
    else:
        print("error:", response.status_code)
        return []