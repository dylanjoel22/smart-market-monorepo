from django.db import models


class Market(models.Model):
    """
    La Marca / Cadena (Ej: Unimarc, Jumbo, Lider).
    """

    name = models.CharField(max_length=100, unique=True, verbose_name="Cadena")
    website = models.URLField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Branch(models.Model):
    """
    Una tienda o zona específica de una cadena.
    Ej: Unimarc Tocopilla, Unimarc Antofagasta.
    """

    market = models.ForeignKey(
        Market, on_delete=models.CASCADE, related_name="branches"
    )
    name = models.CharField(max_length=100, verbose_name="Nombre Sucursal/Zona")
    store_id = models.CharField(max_length=50, verbose_name="ID Interno Tienda")

    class Meta:
        unique_together = ("market", "store_id")
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __str__(self):
        return f"{self.market.name} - {self.name} ({self.store_id})"
