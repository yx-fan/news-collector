from django.core.management.base import BaseCommand
from news.models import News
from news.services.sentiment_analysis import analyze_news_sentiment

class Command(BaseCommand):
    help = "Trigger sentiment analysis for all news articles."

    def handle(self, *args, **kwargs):
        for news in News.objects.all():
            if not news.industries:
                news.industries = []
            if not news.companies:
                news.companies = []
            news.save()
            analyze_news_sentiment(news.url)
            self.stdout.write(self.style.SUCCESS(f"✅ Sentiment analysis triggered for {news.url}"))

        self.stdout.write(self.style.SUCCESS("✅ Sentiment analysis completed."))
