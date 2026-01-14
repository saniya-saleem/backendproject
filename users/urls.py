from django.urls import path
from .views import RegisterAPIView, UserTokenView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterAPIView.as_view()),
    path("login/", UserTokenView.as_view()),   # ✅ JWT login
    path("token/refresh/", TokenRefreshView.as_view()),
]
