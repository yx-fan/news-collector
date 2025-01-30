from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import News
from .serializers import NewsSerializer

# Create your views here.
class NewsViewSet(ReadOnlyModelViewSet):
    queryset = News.objects.all().order_by("-published_at")
    serializer_class = NewsSerializer

# API endpoint to get the latest news
@api_view(["GET"])
def latest_news(request):
    news = News.objects.all().order_by("-published_at")[:10]
    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data)