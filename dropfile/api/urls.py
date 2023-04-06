from django.urls import path, include
from .views import *
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r'files', filesViewSet, basename='files')
# print(router.urls)

urlpatterns = [
    path('files/', filesAPIList.as_view()),
    path('update/<int:pk>/', filesAPIUpdate.as_view()),
    path('delete/<int:pk>/', filesAPIDestroy.as_view()),
]
