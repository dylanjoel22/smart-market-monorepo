from django.db import models


class Product(models.Model):
    """
    Datos Universales: El objeto físico real.
    NO contiene precios ni referencia a ningún supermercado específico.
    """

    ean = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Código EAN",
    )
    name = models.CharField(max_length=255, verbose_name="Nombre Global")
    brand = models.CharField(
        max_length=100, blank=True, null=True, db_index=True, verbose_name="Marca"
    )
    measurement_unit = models.CharField(max_length=20, blank=True, null=True)
    unit_multiplier = models.FloatField(default=1.0)
    package_format = models.CharField(
        max_length=100, null=True, blank=True, help_text="Ej: 1 Kg"
    )
    img_url = models.URLField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.brand} - {self.name} ({self.ean or 'Sin EAN'})"
