from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Banner
from .serializers import BannerSerializer


class BannerAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        banners = Banner.objects.filter(is_active=True)
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data)
