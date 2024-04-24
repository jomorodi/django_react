
from django.urls import path
from . import views
from .views import MyTokenObtainPairView , get_routes

from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView,
)

urlpatterns = [
    path('profile/', views.get_profile),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("", get_routes, name="all_routes" )
]
