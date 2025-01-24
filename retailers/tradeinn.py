from proxies import ProxyRotator
import json


TRADEINN_ID = "67900fe721cc010007e27784"


def get_tradeinn_price(proxy_rotator: ProxyRotator, region_id: str, url: str):
    id_modelo = url.split("/")[-2]
    id_pais = get_tradeinn_id_pais(region_id)
    url_elastic_dc = f"https://dc.tradeinn.com/{id_modelo}"

    headers = {
        'referer': 'https://www.tradeinn.com/'
    }
    
    response = proxy_rotator.get_content(url_elastic_dc, headers=headers)
    product_json = json.loads(response)
    
    product = product_json["_source"]["productes"][0]

    price = None
    for seller in product["sellers"]:
        for precio_pais in seller["precios_paises"]:
            if precio_pais["id_pais"] == id_pais:
                price = precio_pais["precio"]
                break
        if price is not None:
            break

    print(f"url: {url}, country: {id_pais}, price: {price}")

    return price


def get_tradeinn_id_pais(region_id: str) -> int:
    """Returns the Tradeinn ID for the given country ID."""

    region_id_to_id_pais = {
        "678fe4be21cc010007e2777e": 180,
        "67939fcb21cc010007e27790": 70,
        "6793a19121cc010007e27792": 75,
    }
    
    return region_id_to_id_pais.get(region_id, 180)