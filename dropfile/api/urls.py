from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register(r'update_profile_photo', ImageUploadView, basename='photo')
# router.register(r'loadfiles', UploadFilesUser, basename='uploadfiles')

urlpatterns = [
    path('loadfiles/', upload_file),
    path('createpermissons/', insertPermission),
    path('sharedfiles/', FileAccessList.as_view()),
    path('files/', filesAPIList.as_view()),
    path('update/<int:pk>/', filesAPIUpdate.as_view()),
    path('delete/<int:pk>/', filesAPIDestroy.as_view()),
    path('photo/', getProfilePhotoURL.as_view()),
    path('userdata/', getUserData.as_view()),
    path('myfiles/', myFiles.as_view()),
    path('news/', newsAPI.as_view()),
    path('', include(router.urls)),
    path('auth/users/', CreateUserAPIView.as_view(), name='create_user'),
    path('iddev/<int:id>/', GetDeviceID.as_view()),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
