from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/change_data', changeDetails.as_view()),
    path('<int:pk>/', settingData.as_view(), name='settings'),
    path('<int:pk>/change_password', change_password), 
    ]
