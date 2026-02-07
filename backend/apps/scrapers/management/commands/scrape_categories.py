import time
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.scrapers.services.unimarc import UnimarcScraper
from apps.products.models import Product
from apps.markets.models import Market, Branch
from apps.prices.models import PriceSnapshot


class Command(BaseCommand):
    help = "Scrapea categorías completas de Unimarc"

    CATEGORIES = [
        "carnes",
        "frutas verduras",
        "lacteos huevos refrigerados",
        "quesos fiambres",
        "panaderia pasteleria",
        "congelados",
        "despensa",
        "desayuno dulces",
        "bebidas licores",
        "limpieza",
        "bebes niños",
        "perfumeria",
        "mascotas",
        "hogar",
    ]

    def add_arguments(self, parser):
        parser.add_argument("region", type=str, help="Ciudad a scrapear")
        parser.add_argument(
            "--limit",
            type=int,
            default=5,
            help="Límite de páginas por categoría (seguridad)",
        )

    def handle(self, *args, **options):
        region = options["region"]
        limit_pages = options["limit"]
        scraper = UnimarcScraper()

        market, _ = Market.objects.get_or_create(
            name="Unimarc", defaults={"website": "https://www.unimarc.cl"}
        )
        branch, _ = Branch.objects.get_or_create(
            market=market,
            store_id=region,
            defaults={"name": f"Unimarc {region.capitalize()}"},
        )

        self.stdout.write(
            self.style.MIGRATE_HEADING(
                f"Iniciando CRAWLER masivo para {region.upper()}"
            )
        )

        for cat in self.CATEGORIES:
            self.stdout.write(f"\nExplorando categoría: {cat.upper()}...")

            page = 0
            while page < limit_pages:  # Bucle de paginación
                self.stdout.write(f"Página {page}...")
                products_data = scraper.get_products(cat, region, page=page)

                if not products_data:
                    self.stdout.write(
                        self.style.WARNING(f"No hay más productos en {cat}.")
                    )
                    break  # Salta a la siguiente categoría

                saved_count = 0
                for data in products_data:
                    # 1. Gestionar Producto (Universal)
                    ean_val = data.get("ean") or f"INTERNAL_UNIMARC-{data.get('sku')}"
                    product, _ = Product.objects.update_or_create(
                        ean=ean_val,
                        defaults={
                            "name": data.get("name"),
                            "brand": data.get("brand"),
                            "img_url": data.get("img"),
                            "package_format": data.get("package_format"),
                        },
                    )
                    current_price = data.get("price", 0)
                    normal_price = data.get("normal_price") or current_price
                    card_price = data.get("card_price")

                    is_offer = (current_price < normal_price) or (
                        card_price is not None and card_price < current_price
                    )

                    if normal_price > 0 and current_price < normal_price:
                        calculated_discount = int(
                            ((normal_price - current_price) / normal_price) * 100
                        )
                    else:
                        calculated_discount = data.get("discount_percent", 0)

                    # 2. Guardar Snapshot (Geográfico e Histórico)
                    PriceSnapshot.objects.create(
                        product=product,
                        branch=branch,
                        market_sku=data.get("sku"),
                        product_url=data.get("url"),
                        price=current_price,
                        normal_price=normal_price,
                        card_price=card_price,
                        price_per_unit=data.get("price_per_unit"),
                        discount_percent=calculated_discount,
                        is_offer=is_offer,
                        scraped_at=timezone.now(),
                    )
                    saved_count += 1

                self.stdout.write(
                    self.style.SUCCESS(f"Guardados {saved_count} productos.")
                )
                page += 1
                time.sleep(random.uniform(1, 3))  # Delay para no ser bloqueados

        self.stdout.write(self.style.SUCCESS("\nProceso masivo completado con éxito."))
