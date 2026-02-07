from rest_framework import serializers
from .models import PriceSnapshot


class PriceSerializer(serializers.ModelSerializer):
    market_name = serializers.CharField(source="branch.market.name", read_only=True)
    branch_name = serializers.CharField(source="branch.name", read_only=True)

    class Meta:
        model = PriceSnapshot
        fields = [
            "id",
            "market_name",
            "branch_name",
            "price",
            "normal_price",
            "is_offer",
            "price_per_unit",
            "scraped_at",
        ]
