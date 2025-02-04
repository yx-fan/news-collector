from celery import shared_task
import importlib

@shared_task
def fetch_rss_task():
    print("Fetching RSS feed...")
    rss_parser = importlib.import_module("news.services.rss_parser")
    rss_parser.parse_rss()
    print("RSS feed fetched successfully!")