from django.urls import path
from .views import *

urlpatterns = [
    path('', settingData.as_view())
    ]
