from django.urls import path
from .views import (
    LoginView,
    RefreshTokenView,
    LogoutView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh_token'),
    path('logout/', LogoutView.as_view(), name='logout'),
]