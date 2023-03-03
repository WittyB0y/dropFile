from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('', include('loadFile.urls')),
    path('myload/', include('myloads.urls')),
]

handler404 = 'loadFile.views.error_404_view'
