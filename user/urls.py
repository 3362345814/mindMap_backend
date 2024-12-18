from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, LoginView, SendVerificationCodeView, UserProfileView, ResetPasswordView, \
    UpdateUsernameView, UpdateAPIKeyAndBaseURLView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('code/', SendVerificationCodeView.as_view(), name='code'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('update_username/', UpdateUsernameView.as_view(), name='update_username'),
    path('update_key/', UpdateAPIKeyAndBaseURLView.as_view(), name='update_key'),
]
