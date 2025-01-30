from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, latest_news

router = DefaultRouter()
router.register(r"news", NewsViewSet)  # ✅ `/api/news/` 访问所有新闻

urlpatterns = [
    path("", include(router.urls)),  # ✅ 让 DRF 处理所有 ViewSet 路由
    path("latest/", latest_news),  # ✅ `/api/latest/` 访问最新 10 条新闻
]
