from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, UTC
from dotenv import load_dotenv
from bson.objectid import ObjectId
from db import Database, iterate_collection
from proxies import ProxyRotator, get_proxies
from retailers.amazon import get_amazon_price
from retailers.tradeinn import get_tradeinn_price


AMAZON_ID = "678fe61421cc010007e27780"
TRADEINN_ID = "67900fe721cc010007e27784"


def process_product(db, proxy_rotator, product):
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

    price_document = {
        "product_id": ObjectId(product_id),
        "retailer_id": ObjectId(retailer_id),
        "country_id": ObjectId(country_id),
        "price": price,
        "time_checked": datetime.now(UTC)
    }

    prices_collection = db.db["prices"]
    prices_collection.insert_one(price_document)


def main() -> None:
    load_dotenv()

    db = Database()

    proxies = get_proxies()
    proxy_rotator = ProxyRotator(proxies)

    NUM_WORKERS = 50
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        for product in iterate_collection(db, "monitored"):
            executor.submit(process_product, db, proxy_rotator, product)


if __name__ == "__main__":
    main()