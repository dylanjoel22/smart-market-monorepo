from django.contrib import admin
from .models import PriceSnapshot


@admin.register(PriceSnapshot)
class PriceSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "product_name",
        "branch",
        "price",
        "normal_price",
        "discount_percent",
        "is_offer",
        "is_available",
        "scraped_at",
    )
    search_fields = ("product__name", "product__brand", "branch__name")
    list_filter = ("branch", "is_offer", "is_available", "scraped_at")
    ordering = ("-scraped_at",)
    list_per_page = 50
    readonly_fields = ("scraped_at", "discount_percent")
    date_hierarchy = "scraped_at"

    fieldsets = (
        ("Producto y Sucursal", {"fields": ("product", "branch", "market_sku")}),
        (
            "Precios",
            {"fields": ("price", "normal_price", "price_per_unit", "discount_percent")},
        ),
        ("Disponibilidad", {"fields": ("is_available", "stock", "is_offer")}),
        (
            "Información Extra",
            {
                "fields": ("product_url", "dynamic_data", "scraped_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = "Producto"

    def get_queryset(self, request):
        """Optimizar queries con select_related"""
        qs = super().get_queryset(request)
        return qs.select_related("product", "branch", "branch__market")
