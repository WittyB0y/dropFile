from django.urls import path

from news.views import NewsPage

urlpatterns = [
    path('', NewsPage.as_view(), name='news'),
    ]