from .views import *
from django.urls import path, include

urlpatterns = [
path('', get_files, name='myFiles'),
path('delete/<slug:slug>/', delete_file)
]