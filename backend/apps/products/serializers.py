from rest_framework import serializers
from .models import Product
from apps.prices.serializers import PriceSerializer


class ProductDetailSerializer(serializers.ModelSerializer):
    price_history = PriceSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "ean",
            "name",
            "brand",
            "package_format",
            "img_url",
            "price_history",
        ]


class ProductListSerializer(serializers.ModelSerializer):
    lower_price = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "ean", "name", "brand", "img_url", "lower_price"]
