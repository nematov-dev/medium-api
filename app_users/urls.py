from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path

from app_users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterApiView.as_view(), name='register'),
    path('verify/email/', views.VerifyEmailApiView.as_view(), name='verify'),
    path('login/', views.LoginApiView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]