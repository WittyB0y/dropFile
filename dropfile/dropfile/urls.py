from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('loadFile.urls')),
]
handler404 = 'loadFile.views.error_404_view'