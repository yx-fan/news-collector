from djongo import models
from bson import ObjectId

class News(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    url = models.URLField(unique=True, blank=False, null=False)
    title = models.CharField(max_length=255, blank=False, null=False)
    source = models.CharField(max_length=100, blank=False, null=False)
    category = models.CharField(max_length=50, choices=[
        ("market", "Market"),
        ("crypto", "Crypto"),
        ("stocks", "Stocks"),
        ("economy", "Economy"),
    ], blank=False, null=False)
    published_at = models.DateTimeField(blank=False, null=False)

    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)

    # New fields for sentiment analysis
    sentiment_score = models.FloatField(blank=True)
    companies = models.JSONField(default=list, blank=True)
    industries = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-published_at"]


