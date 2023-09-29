import requests
from datetime import datetime, timedelta

from twilio.rest import Client

import os




STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
STOCK_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": STOCK_API_KEY
}


NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
yesterday = datetime.now() - timedelta(days=1)
two_days_ago = yesterday - timedelta(days=1)
YESTERDAY = yesterday.strftime("%Y-%m-%d")
TWO_DAYS_AGO = two_days_ago.strftime("%Y-%m-%d")
NEWS_PARAMETERS = {
    "q": COMPANY_NAME,
    "from": TWO_DAYS_AGO,
    "to": YESTERDAY,
    "language": "en",
    "sortBy": "relevancy",
    "apiKey": NEWS_API_KEY
}

TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_API_KEY = os.environ.get("TWILIO_API_KEY")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")
MY_NUMBER = os.environ.get("MY_NUMBER")


def get_daily_time_series():
    response = requests.get(STOCK_ENDPOINT, STOCK_PARAMETERS)
    response = response.json()
    return response

def five_percent_shift(daily_time_series) -> bool:
    data = daily_time_series["Time Series (Daily)"]
    data_list = [value for (_, value) in data.items()]
    yesterday_open = float(data_list[0]["1. open"])
    two_days_ago_close = float(data_list[1]["4. close"])

    delta = (yesterday_open - two_days_ago_close)
    percent_change = (delta / two_days_ago_close) * 100
    return (percent_change > 5.0, percent_change)


def get_news_top_three():
    response = requests.get(NEWS_ENDPOINT, NEWS_PARAMETERS)
    news = response.json()['articles'][:3]
    return news


def format_articles(news_articles):
    return [{"headline": article["title"], "brief": article["description"]} for article in news_articles]
    
def sms_news(news_articles, percent_change):
    dir_symbol = "🔺" if percent_change > 0 else "🔻"
    client = Client(TWILIO_SID, TWILIO_API_KEY)
    client.messages.create(
        from_=TWILIO_NUMBER,
        to=MY_NUMBER,
        body=STOCK + ": " + dir_symbol + "%" + "{:.2f}".format((abs(percent_change)))
    )
    for article in news_articles:
        headline = article["headline"]
        brief = article["brief"]
        client.messages.create(
            from_=TWILIO_NUMBER,
            to=MY_NUMBER,
            body= f"Headline: {headline}\nBrief: {brief}"
        )
    
def main():
    daily_time_series = get_daily_time_series()
    large_price_change, delta = five_percent_shift(daily_time_series)
    if large_price_change:
        articles = get_news_top_three()
        articles = format_articles(articles)
        sms_news(articles, delta)

if __name__ == "__main__":
    main()


