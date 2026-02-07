from rest_framework import serializers
from .models import Market, Branch


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "market", "name", "store_id"]


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ["id", "name", "website", "is_active"]
