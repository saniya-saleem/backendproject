from rest_framework import serializers
from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    image = serializers.URLField()

    class Meta:
        model = Banner
        fields = ["id", "image"]
