import os
import feedparser
import pytz
import time
from datetime import datetime
from newspaper import Article  # Added for fetching full article content
from news.models import News
from news.tasks.sentiment_tasks import analyze_news_sentiment_task
from .rss_sources import RSS_FEEDS
from .sentiment_analysis import analyze_news_sentiment

USE_CELERY = os.getenv("USE_CELERY", "False").lower() == "true"

def parse_rss():
    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)  # Fetch RSS data

        for entry in feed.entries:
            print(f"Get news {entry.get('title', 'No Title')} from {source}")
            title = entry.get("title", "No Title")
            link = entry.get("link", "")

            # Parse published time
            published_at = parse_published_time(source, entry)
            
            # Parse summary
            summary = parse_summary(source, entry)
            
            # Parse source name
            source_name = parse_source_name(source, entry)
            
            # Fetch full article content
            content = fetch_full_article(link)
            
            # Auto-categorize news
            category = categorize_news(title, summary, content)

            # print(f"Saving news: title={title}, source={source_name}, published_at={published_at}, summary={summary}, content={content}, category={category}")

            # Save news to the database
            news, created = News.objects.update_or_create(
                url=link,
                defaults={
                    "title": title,
                    "source": source_name,
                    "published_at": published_at,
                    "summary": summary,
                    "content": content,
                    "category": category,
                    "sentiment_score": None,
                    "companies": [],
                    "industries": [],
                }
            )

            print(f"✅ News {news.title} saved to the database.")
            print("created", created)

            # Trigger sentiment analysis task
            if created:
                if USE_CELERY:
                    print(f"ℹ️ Triggering sentiment analysis task for {news.url}")
                    analyze_news_sentiment_task.delay(news.url)
                else:
                    print(f"ℹ️ Processing news {news.url}")
                    analyze_news_sentiment(news.url)

    print("✅ RSS parsing and saving completed.")

# Parse published time
def parse_published_time(source, entry):
    published = entry.get("published", "")
    try:
        if source == "Yahoo Finance":
            dt = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
        elif source == "CNBC":
            dt = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %Z")
        else:
            dt = datetime.now()  # Default case
        return dt.replace(tzinfo=pytz.utc)  # Convert to UTC
    except Exception:
        return datetime.now().replace(tzinfo=pytz.utc)

# Parse summary
def parse_summary(source, entry):
    return entry.get("summary", "No summary available.")

# Parse source name
def parse_source_name(source, entry):
    if "source" in entry and isinstance(entry["source"], dict):
        return entry["source"].get("title", source)
    return source

# Fetch full article content using newspaper3k
def fetch_full_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text if article.text else "No content available."
    except Exception as e:
        print(f"❌ Failed to fetch content for {url}: {e}")
        return "No content available."

# Auto-categorize news
def categorize_news(title, summary, content):
    keywords = {
        "market": ["stock market", "S&P 500", "Nasdaq", "Dow Jones"],
        "crypto": ["Bitcoin", "Ethereum", "crypto", "blockchain"],
        "stocks": ["shares", "earnings", "IPO", "dividends"],
        "economy": ["GDP", "inflation", "interest rates", "Federal Reserve"],
    }
    text = f"{title} {summary} {content}".lower()
    
    for category, words in keywords.items():
        if any(word in text for word in words):
            return category 
    return "market"  # Default category

print("✅ RSS Parser with newspaper3k Ready!")
