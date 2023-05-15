from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myloads/', include('myloads.urls')),
    path('settings/', include('setting.urls')),
    path('api/v1/', include('api.urls')),
    path('news/', include('news.urls')),
    path('', include('user.urls')),
    path('', include('loadFile.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'loadFile.views.error_404_view'
