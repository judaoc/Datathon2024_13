import json
from json_claude import analyzeArticles, analyzeSpecificArticles
from yahoo_fin import news
from dotenv import load_dotenv
import os

load_dotenv()
SYMBOLS500 = os.getenv('SYMBOLS500').split(',')


def getNews():
    all_news_data = []
    for symbol in SYMBOLS500:
        try:
            symbol_news = news.get_yf_rss(symbol)[:1]
            all_news_data.extend(symbol_news)
        except Exception as e:
            print(f"Error fetching news for {symbol}: {e}")

    all_news_data_json = json.dumps(all_news_data, indent=4)
    good_news_indexes = analyzeArticles(all_news_data_json)
    if good_news_indexes[0].isdigit():
        return [all_news_data[int(i)] for i in good_news_indexes if int(i) < len(all_news_data)]
    else: return []
    
def getSpecificNews(symbol):
    try:
        symbol_news = news.get_yf_rss(symbol)
    except Exception as e:
        print(f"Error fetching news for {symbol}: {e}")
    all_news_data_json = json.dumps(symbol_news, indent=4)
    good_news_indexes = analyzeSpecificArticles(all_news_data_json, symbol)
    if good_news_indexes[0].isdigit():
        return [symbol_news[int(i)] for i in good_news_indexes if int(i) < len(symbol_news)]
    else: return []