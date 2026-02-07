from django.db import models
from django.utils import timezone
from apps.products.models import Product
from apps.markets.models import Market, Branch


class PriceSnapshot(models.Model):
    """
    Representa un precio encontrado en un mercado específico en un momento dado.
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="price_history"
    )
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="price_history"
    )

    market_sku = models.CharField(
        max_length=50, db_index=True, verbose_name="SKU Tienda"
    )
    product_url = models.URLField(max_length=500, blank=True, null=True)

    price = models.IntegerField(verbose_name="Precio Oferta (Actual)")
    normal_price = models.IntegerField(
        verbose_name="Precio Normal", null=True, blank=True
    )
    card_price = models.IntegerField(
        verbose_name="Precio Club/Tarjeta", null=True, blank=True
    )
    price_per_unit = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Precio x Unidad"
    )

    discount_percent = models.IntegerField(default=0)

    is_offer = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)

    dynamic_data = models.JSONField(
        default=dict, blank=True, verbose_name="Datos Variables"
    )

    scraped_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        verbose_name = "Historial de Precio"
        verbose_name_plural = "Historial de Precios"
        ordering = ["-scraped_at"]
        indexes = [
            models.Index(fields=["product", "branch", "scraped_at"]),
        ]

    def __str__(self):
        return f"{self.branch}: {self.product.name} - ${self.price}"
