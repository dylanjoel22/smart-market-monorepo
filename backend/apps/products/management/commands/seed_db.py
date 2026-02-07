from django.core.management.base import BaseCommand
from apps.markets.models import Market
from apps.prices.models import Price
from apps.products.models import Category, Product
import random


class Command(BaseCommand):
    help = "Este comando es para verificar que todo funciona como deberia"

    def handle(self, *args, **kwargs):
        # Price.objects.all().delete()
        # Product.objects.all().delete()
        # Category.objects.all().delete()
        # Market.objects.all().delete()

        lider, created = Market.objects.get_or_create(
            name="Líder",
            defaults={
                "location": "Santiago, Chile",
                "website": "https://www.lider.cl",
                "is_active": True,
            },
        )
        if created:
            self.stdout.write(f"Mercado creado: {lider.name}")

        storeroom, _ = Category.objects.get_or_create(name="Despensa")

        rice, created = Product.objects.get_or_create(
            ean="7801234567890", defaults={"name": "Arroz", "category": storeroom}
        )
        if created:
            self.stdout.write(f"Producto creado: {rice.name}")

        test_price = random.choice([1800, 1500, 2000])

        price, created = Price.objects.get_or_create(
            product=rice,
            market=lider,
            value=test_price,
            prod_url="https://www.lider.cl/arroz",
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Precio creado: {price.value}"))
        else:
            self.stdout.write(self.style.WARNING(f"Precio ya existente: {price.value}"))
