from django.contrib import admin
from django.utils.html import format_html
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "show_image",
        "ean",
        "brand",
        "name",
        "measurement_unit",
        "package_format",
        "updated_at",
    )
    list_display_links = ("ean", "name")
    search_fields = ("name", "brand", "ean")
    list_filter = ("brand", "created_at")
    ordering = ("-updated_at",)
    list_per_page = 50
    readonly_fields = ("created_at", "updated_at", "show_image")

    fieldsets = (
        ("Información Básica", {"fields": ("ean", "name", "brand", "show_image")}),
        (
            "Detalles Técnicos",
            {
                "fields": (
                    "measurement_unit",
                    "unit_multiplier",
                    "package_format",
                    "img_url",
                )
            },
        ),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def show_image(self, obj):
        if obj.img_url:
            return format_html(
                '<img src="{}" style="width: 60px; height: auto; border-radius: 4px;" />',
                obj.img_url,
            )
        return "Sin imagen"

    show_image.short_description = "Imagen"
