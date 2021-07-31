import random
import requests
from datetime import datetime, timedelta
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "W1F681UNX6LX0T5Q"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "c1206c71c73a47b39b10e7ec2b69ab7b"

account_sid = "AC1769847cda015262b401e487fe9a8bf2"
auth_token = "5e53374aef8a359a7e3cd25f17a5108e"

STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "apikey": "W1F681UNX6LX0T5Q"
}

response = requests.get(url="https://www.alphavantage.co/query", params=STOCK_PARAMS)

process_yesterday = datetime.now() - timedelta(2)
yesterday = str(datetime.strftime(process_yesterday, '%Y-%m-%d'))
yesterday_data = response.json()["Time Series (Daily)"][yesterday]
yesterdays_closing_price = float(yesterday_data["4. close"])

process_day_before_yesterday = datetime.now() - timedelta(3)
day_before_yesterday = str(datetime.strftime(process_day_before_yesterday, '%Y-%m-%d'))
day_before_yesterday_data = response.json()["Time Series (Daily)"][day_before_yesterday]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

difference_in_closing_price = abs(yesterdays_closing_price - day_before_yesterday_closing_price)

difference_percentage = difference_in_closing_price / yesterdays_closing_price * 100

if difference_percentage > 1:
    NEWS_PARAMS = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(url="https://newsapi.org/v2/everything", params=NEWS_PARAMS)
    news_data = news_response.json()["articles"]
    first_three_articles = news_data[0:3]

    articles_list = [f"Headline: {article['title']}. \n Brief: {article['description']}" for article in
                     first_three_articles]

    client = Client(account_sid, auth_token)
    random_int = random.randint(0, 2)
    message = client.messages \
        .create(body=f"{STOCK_NAME}: 🔺1%\n {articles_list[random_int]}", from_='+14159937741',
                to='+94703925064')
    print(message.status)