from dotenv import load_dotenv
from db import Database, iterate_collection
from proxies import ProxyRotator, get_proxies
from amazon import get_amazon_price
from tradeinn import get_tradeinn_price
from datetime import datetime, UTC
from bson.objectid import ObjectId


AMAZON_ID = "678fe61421cc010007e27780"
TRADEINN_ID = "67900fe721cc010007e27784"


def store_price(db, product_id: str, region_id: str, retailer_id: str, price: float):
    """Store the price in the database."""

    price_document = {
        "product_id": ObjectId(product_id),
        "retailer_id": ObjectId(retailer_id),
        "country_id": ObjectId(region_id),
        "price": price,
        "time_checked": datetime.now(UTC)
    }

    prices_collection = db.db["prices"]
    prices_collection.insert_one(price_document)


def main():
    load_dotenv()
 
    db = Database()

    proxies = get_proxies()
    proxy_rotator = ProxyRotator(proxies)

    for product in iterate_collection(db, "monitored"):
        
        product_id = str(product["product_id"])
        retailer_id = str(product["retailer_id"])
        country_id = str(product["country_id"])
        url = product["url"]

        if retailer_id == AMAZON_ID:
            price = get_amazon_price(proxy_rotator, country_id, url)
        elif retailer_id == TRADEINN_ID:
            price = get_tradeinn_price(proxy_rotator, country_id, url)
        else:
            print(f"Unknown retailer: {product}")

        store_price(db, product_id, country_id, retailer_id, price)


if __name__ == "__main__":
    main()