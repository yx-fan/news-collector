from django.core.management.base import BaseCommand
from news.rss_parser import parse_rss

# Create a custom management command to fetch RSS feed
class Command(BaseCommand):
    help = "Fetch RSS feed"

    def handle(self, *args, **options):
        parse_rss()
        self.stdout.write(self.style.SUCCESS("RSS feed fetched successfully!"))