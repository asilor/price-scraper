from database import Database, store_price
from bson.objectid import ObjectId
from proxies import ProxyRotator
import json


TRADEINN_ID = "67900fe721cc010007e27784"


def get_tradeinn_price(db: Database, proxy_rotator: ProxyRotator, product: dict) -> None:
    url = product["url"]
    id_modelo = url.split("/")[-2]

    url_elastic_dc = f"https://dc.tradeinn.com/{id_modelo}"

    headers = {
        'referer': 'https://www.tradeinn.com/'
    }
    
    response = proxy_rotator.get_content(url_elastic_dc, headers=headers)
    product_json = json.loads(response)
    
    precio_paises = product_json["_source"]["productes"][0]["sellers"][0]["precios_paises"]
    
    for precio_pais in precio_paises:
        region_id = get_region_id(precio_pais["id_pais"])
        if region_id:
            price = precio_pais["precio"]

            product["region_id"] = ObjectId(region_id)

            store_price(db, product, price)
            print(f"url: {url}, region_id: {region_id}, price: {price}")


def get_region_id(id_pais: str) -> int:
    """Returns the region_id given the id_pais."""

    id_pais_to_region_id = {
        180: "678fe4be21cc010007e2777e",
        70: "67939fcb21cc010007e27790",
        75: "6793a19121cc010007e27792",
    }

    region_id = id_pais_to_region_id.get(id_pais, None)
    
    return region_id
