from django.db.models import Min
from rest_framework import viewsets
from .models import Product
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = Product.objects.all()

        if self.action == "list":
            queryset = queryset.annotate(
                lower_price=Min("price_history__price")
            ).order_by("created_at")

        else:
            queryset = queryset.prefetch_related(
                "price_history",
                "price_history__branch",
                "price_history__branch__market",
            ).order_by("created_at")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return ProductDetailSerializer
