import feedparser
import pytz
from datetime import datetime
from .models import News
from .rss_sources import RSS_FEEDS

def parse_rss():
    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url) # Obtain the feed data

        for entry in feed.entries:
            print(f"Get news {entry.get('title', 'No Title')} from {source}")
            title = entry.get("title", "No Title")
            link = entry.get("link", "")

            # Get the published time
            published_at = parse_published_time(source, entry)

            # Get the summary
            summary = parse_summary(source, entry)

            # Get the source name
            source_name = parse_source_name(source, entry)

            # Save the news to the database
            News.objects.update_or_create(
                url=link,
                defaults={
                    "title": title,
                    "source": source_name,
                    "published_at": published_at,
                    "summary": summary,
                }
            )

    print("✅ RSS parsing and saving completed.")

# Parse the published time
def parse_published_time(source, entry):
    published = entry.get("published", "")
    try:
        if source == "Yahoo Finance":
            dt = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
        elif source == "CNBC":
            dt = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %Z")
        else:
            dt = datetime.now() # Add more cases if needed
        
        # Convert the datetime to UTC
        return dt.replace(tzinfo=pytz.utc)

    except Exception:
        return datetime.now().replace(tzinfo=pytz.utc)

# Parse the summary
def parse_summary(source, entry):
    if source == "Yahoo Finance":
        return entry.get("summary", "No summary available.")
    elif source == "CNBC":
        return entry.get("summary", "No summary available.")
    else:
        return entry.get("summary", "") # Add more cases if needed

# Parse the source name
def parse_source_name(source, entry):
    if "source" in entry and isinstance(entry["source"], dict):
        return entry["source"].get("title", source)
    return source
