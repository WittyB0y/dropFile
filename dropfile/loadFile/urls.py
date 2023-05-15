from django.urls import path
from .views import *

urlpatterns = [
    path('', LoadDataView.as_view(), name='home'),
    path('main/', newMainPage.as_view()),
    path('media/', say_hi),
    path('myfiles/', myfiles.as_view()),
    path('adduser/', addUserAccess, name='addUser'),
    path('adduser/1/', UserAccesss, name='addUser1'),
    path('<slug:slug>/', loadFile.as_view()),
    path('download/<slug:slugy>/', download_file),
]

