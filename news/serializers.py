from rest_framework import serializers
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["title", "url", "source", "summary", "content", "category", "published_at", "sentiment_score"]