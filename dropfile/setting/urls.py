from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/change_data', changeDetails.as_view()),
    path('<int:pk>/', settingData.as_view(), name='settings'),
    path('<int:pk>/change_password', change_password), 
    path('<int:pk>/delete_profile', delete_profile, name='delete_profile'),
    path('<int:pk>/delete_files', delete_all_files, name='delete_file'),
    path('<int:pk>/change_photo', change_photo),
    ]
