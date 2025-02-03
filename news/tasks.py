from celery import shared_task
from news.services.rss_parser import parse_rss

@shared_task
def fetch_rss():
    print("Fetching RSS feed...")
    parse_rss()
    print("RSS feed fetched successfully!")
