from django.core.management.base import BaseCommand
from apps.scrapers.services.unimarc import UnimarcScraper
import json
import os


class Command(BaseCommand):
    help = "Prueba el scraper y guarda un ejemplo de los datos"

    def add_arguments(self, parser):
        parser.add_argument(
            "query", type=str, nargs="?", default="arroz", help="Producto a buscar"
        )

    def handle(self, *args, **options):
        scraper = UnimarcScraper()
        producto_a_buscar = options["query"]

        self.stdout.write(
            self.style.MIGRATE_HEADING(f"🔎 Buscando: '{producto_a_buscar}'")
        )

        # Usamos Tocopilla para la prueba
        resultados = scraper.get_products(producto_a_buscar, "tocopilla")

        if resultados:
            print(f"\n✅ Se encontraron {len(resultados)} productos.")
            primer_producto = resultados[0]
            print(
                f"   Ejemplo: {primer_producto['name']} -> ${primer_producto['price']}"
            )
            # Guardamos la lista completa en un archivo
            archivo_salida = "unimarc_data_dump.json"
            with open(archivo_salida, "w", encoding="utf-8") as f:
                json.dump(resultados, f, indent=4, ensure_ascii=False)

            self.stdout.write(
                self.style.SUCCESS(
                    f"\n📁 JSON guardado exitosamente en: {os.path.abspath(archivo_salida)}"
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    "👉 Abre ese archivo en VS Code para ver todos los campos disponibles (brand, sku, etc.)"
                )
            )

        else:
            self.stdout.write(self.style.ERROR("❌ No se encontraron productos."))
