import requests
from datetime import datetime, timedelta, timezone
import json
from json_claude import analyzeArticles


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
        best_articles_indexes = analyzeArticles(recent_articles_json, symbol)
        if best_articles_indexes[0].isdigit():
            best_recent_articles = [recent_articles[int(i)] for i in best_articles_indexes if int(i) < len(recent_articles)]
            return best_recent_articles
        else: return []
    else:
        print("error:", response.status_code)
        return []