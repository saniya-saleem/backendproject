from django.urls import path
from .views import BannerAPIView

path("banners/", BannerAPIView.as_view()),
