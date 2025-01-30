from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, latest_news

router = DefaultRouter()
router.register(r"news", NewsViewSet) 

urlpatterns = [
    path("", include(router.urls)),  # ✅ `/api/news/` visit all news
    path("latest/", latest_news),  # ✅ `/api/latest/` visit the latest news
]
