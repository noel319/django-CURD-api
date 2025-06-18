from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationAPIView,
    CustomTokenObtainPairView,
    UserProfileAPIView,
    change_password,
    logout,
)

app_name = 'authentication'

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('change-password/', change_password, name='change-password'),
    path('logout/', logout, name='logout'),
]