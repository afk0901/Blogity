"""
This module handles JWS authentication
"""
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

urlpatterns = [
    # Get the token
    path("", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Refresh the token
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Verify the token
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
]
