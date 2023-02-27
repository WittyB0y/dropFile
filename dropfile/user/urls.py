from django.urls import path
from .views import RegisterUser, LoginUser, logout
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
