import requests
import json
import random
import string


class UnimarcScraper:
    def __init__(self):
        self.url_api = "https://bff-unimarc-ecommerce.unimarc.cl/catalog/product/search"

        self.anonymous_id = self.generate_id(21)
        self.session_id = self.generate_id(21)

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "es-ES,es;q=0.9",
            "Origin": "https://www.unimarc.cl",
            "Referer": "https://www.unimarc.cl/",
            "Content-Type": "application/json",
            "channel": "UNIMARC",
            "source": "web",
            "version": "1.0.0",
            "anonymous": self.anonymous_id,
            "session": self.session_id,
            "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }

        self.region_codes = {
            "antofagasta": "55",
            "tocopilla": "59",
            "santiago": "1",
        }

    def generate_id(self, length=21):
        """
        Genera IDs alfanuméricos como los del navegador
        """
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(length))

    def get_products(self, query, city_name, page=0):
        city_key = city_name.lower().strip()
        region_id = self.region_codes.get(city_key, "55")

        print(f"Zona '{city_name.capitalize()}' ID: {region_id}")

        offset_from = page * 50
        offset_to = offset_from + 49

        cookies = {
            "co_sc": region_id,
            "promotionalModal": "true",
        }

        payload = {
            "from": str(offset_from),
            "to": str(offset_to),
            "orderBy": "",
            "searching": query,
            "promotionsOnly": False,
            "userTriggered": True,
        }

        print(f"Conectando a la API BFF: {self.url_api}...")

        try:
            response = requests.post(
                self.url_api,
                headers=self.headers,
                cookies=cookies,
                json=payload,
                timeout=15,
            )

            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                print(f"Respuesta: {response.text[:200]}")
                return []

            data = response.json()

            return self._parse_bff_response(data, region_name=city_name)

        except Exception as e:
            print(f"Error {str(e)}")
            return []

    def _parse_bff_response(self, data, region_name):
        """
        Busca productos en la respuesta JSON de manera recursiva, tenga la forma que tenga
        """
        raw_products = []

        if isinstance(data, dict) and "availableProducts" in data:
            raw_products = data["availableProducts"]
        elif isinstance(data, dict):
            if "data" in data and isinstance(data["data"], list):
                raw_products = data["data"]
            elif "products" in data:
                raw_products = data["products"]
            elif "hits" in data:
                raw_products = data["hits"]
        elif isinstance(data, list):
            raw_products = data

        if not raw_products:
            raw_products = self._recursive_search(data)

        if not raw_products:
            print(
                "JSON recibido pero no encontré 'availableProducts' ni listas conocidas"
            )
            return []

        products_clean = []
        for item in raw_products:
            try:
                card_price = None
                discount_percent = 0

                if "item" in item and "price" in item:
                    prod_data = item["item"]
                    price_data = item["price"]
                    promo_data = item.get("promotion", {})

                    name = prod_data.get("nameComplete") or prod_data.get("name")
                    sku = prod_data.get("sku") or prod_data.get("itemId")
                    brand = prod_data.get("brand")
                    ean = prod_data.get("ean")

                    price_str = price_data.get("price", "0")
                    price = self._clean_price_string(price_str)
                    normal_price = self._clean_price_string(
                        price_data.get("listPrice", price_str)
                    )
                    card_price = None
                    payment_methods = promo_data.get("pricePaymentsMethods", [])
                    if payment_methods:
                        price_list = [
                            m.get("price") for m in payment_methods if m.get("price")
                        ]
                        if price_list:
                            card_price = self._clean_price_string(min(price_list))

                    if normal_price > price:
                        discount_percent = int(
                            ((normal_price - price) / normal_price) * 100
                        )

                    img = ""
                    if "images" in prod_data and prod_data["images"]:
                        img = prod_data["images"][0]

                    link_text = prod_data.get("itemId")
                    package_format = prod_data.get("netContent")
                    price_per_unit = prod_data.get("pricePerUnit")

                else:
                    name = item.get("name") or item.get("productName")
                    sku = item.get("sku")
                    ean = item.get("ean")
                    brand = item.get("brand")
                    price = self._extract_price_standard(item)
                    normal_price = self._extract_normal_price(item)
                    img = item.get("images", [{}])[0].get("url", "")
                    link_text = item.get("linkText") or item.get("slug")
                    package_format = item.get("netContent")
                    price_per_unit = item.get("pricePerUnit")

                if price > 0 and name:
                    # Construir el diccionario de forma consistente
                    if "item" in item and "price" in item:
                        prod_data_dict = item["item"]
                    else:
                        prod_data_dict = item

                    products_clean.append(
                        {
                            "name": name,
                            "sku": sku,
                            "ean": ean,
                            "brand": brand,
                            "url": f"https://www.unimarc.cl/product/{link_text}",
                            "img": img,
                            "price": price,
                            "normal_price": normal_price,
                            "card_price": card_price,
                            "discount_percent": discount_percent,
                            "package_format": package_format,
                            "price_per_unit": price_per_unit,
                        }
                    )
            except Exception as e:
                continue

        if products_clean:
            print(f"{len(products_clean)} productos encontrados en {region_name}.")

        return products_clean

    def _recursive_search(self, data):
        """
        Busca una lista de objetos que aparezca 'productId' o 'productName'
        """
        if isinstance(data, dict):
            if "productId" in data or "productName" in data:
                return [data]

            for key, value in data.items():
                res = self._recursive_search(value)
                if res:
                    return res

        elif isinstance(data, list):
            if len(data) > 0 and isinstance(data[0], dict):
                if (
                    "productId" in data[0]
                    or "productName" in data[0]
                    or "sellers" in data[0]
                ):
                    return data

            for item in data:
                res = self._recursive_search(item)
                if res:
                    return res
        return None

    def _clean_price_string(self, price_str):
        """
        Convierte '$1.000' -> 1000
        """
        if isinstance(price_str, (int, float)):
            return int(price_str)
        if isinstance(price_str, str):
            clean = price_str.replace("$", "").replace(".", "").replace(",", "")
            try:
                return int(clean)
            except:
                return 0
        return 0

    def _extract_price_standard(self, item):
        """
        Para el formato antiguo (sellers/commertialOffer)
        """
        try:
            if item.get("sellers"):
                price = item["sellers"][0].get("commertialOffer", {}).get("Price")
                if price:
                    return int(price)
            if item.get("price"):
                return int(item["price"])
            if item.get("prices"):
                return int(item.get("prices", {}).get("bestPrice", 0))
        except:
            return 0
        return 0

    def _extract_normal_price(self, item):
        """
        Extrae el precio normal/list price de diferentes formatos
        """
        try:
            if item.get("sellers"):
                price = item["sellers"][0].get("commertialOffer", {}).get("ListPrice")
                if price:
                    return int(price)
            if item.get("listPrice"):
                return int(item["listPrice"])
            if item.get("prices"):
                return int(item.get("prices", {}).get("listPrice", 0))
        except:
            return 0
        return 0
