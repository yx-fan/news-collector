from celery import shared_task
import importlib

@shared_task
def analyze_news_sentiment_task(news_url):
    print("Processing news...")
    sentiment_analysis = importlib.import_module("news.services.sentiment_analysis")
    sentiment_analysis.analyze_news_sentiment(news_url)
    print("News processed successfully!")

