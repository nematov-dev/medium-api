from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenBlacklistView,
)
from django.urls import path

from app_users import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterApiView.as_view(), name='register'),
    path('login/', views.LoginApiView.as_view(), name='token_obtain_pair'),
    path('logout/', TokenBlacklistView.as_view(), name='logout'),
    path('verify/email/', views.VerifyEmailApiView.as_view(), name='verify'),
    path('me/',views.DashboardAPIView.as_view(), name='dashboard'),
    path('update/password/', views.UpdatePasswordAPIView.as_view(), name='update_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]