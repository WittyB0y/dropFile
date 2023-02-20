from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', load_data),
    path('<slug:slug>/', loadFile.as_view()),
    path('download/<slug:slugy>/', download_file)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
