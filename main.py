from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, UTC
from dotenv import load_dotenv
from bson.objectid import ObjectId
from database import get_database, iterate_collection
from proxies import ProxyRotator, get_proxies
from retailers.amazon import get_amazon_price, AMAZON_ID
from retailers.tradeinn import get_tradeinn_price, TRADEINN_ID


def store_price(db, product_id, retailer_id, region_id, price) -> None:
    """Stores the given price in the database."""

    price_document = {
        "metadata": {
            "product_id": ObjectId(product_id),
            "retailer_id": ObjectId(retailer_id),
            "region_id": ObjectId(region_id)
        },
        "timestamp": datetime.now(UTC),
        "price": price
    }

    prices_collection = db["prices"]
    prices_collection.insert_one(price_document)


def process_product(db, proxy_rotator, product) -> None:
    product_id = str(product["product_id"])
    retailer_id = str(product["retailer_id"])
    region_id = str(product["region_id"])
    url = product["url"]

    if retailer_id == AMAZON_ID:
        price = get_amazon_price(proxy_rotator, region_id, url)
        store_price(db, product_id, retailer_id, region_id, price)
    elif retailer_id == TRADEINN_ID:
        price = get_tradeinn_price(proxy_rotator, region_id, url)
        store_price(db, product_id, retailer_id, region_id, price)
    else:
        print(f"Unknown retailer: {product}")


def main() -> None:
    print("Starting product scrapeing")

    load_dotenv()

    db = get_database()
    proxies = get_proxies()
    proxy_rotator = ProxyRotator(proxies)

    NUM_WORKERS = 10
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        for product in iterate_collection(db, "monitored"):
            executor.submit(process_product, db, proxy_rotator, product)


if __name__ == "__main__":
    main()