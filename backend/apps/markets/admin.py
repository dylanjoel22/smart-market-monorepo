from django.contrib import admin
from .models import Market, Branch


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "is_active", "branch_count")
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("name",)
    fieldsets = (
        ("Información Básica", {"fields": ("name", "website", "is_active")}),
    )

    def branch_count(self, obj):
        count = obj.branches.count()
        return f"{count} sucursal(es)"

    branch_count.short_description = "Sucursales"


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "market", "store_id", "price_history_count")
    search_fields = ("name", "market__name", "store_id")
    list_filter = ("market",)
    ordering = ("market", "name")
    fieldsets = (
        ("Información de Sucursal", {"fields": ("market", "name", "store_id")}),
    )

    def price_history_count(self, obj):
        count = obj.price_history.count()
        return f"{count} registro(s) de precio"

    price_history_count.short_description = "Historial de Precios"

    def get_queryset(self, request):
        """Optimizar queries con select_related"""
        qs = super().get_queryset(request)
        return qs.select_related("market")
