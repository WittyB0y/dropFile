from .views import *
from django.urls import path, include

urlpatterns = [
path('', get_files, name='myFiles'),
path('delete/<slug:slug>/', delete_file),
path('changeaccsess/<slug:slug>/<str:bool_type>',change_accsses),
]