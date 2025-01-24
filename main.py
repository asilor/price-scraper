from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from database import get_database, iterate_collection
from proxies import ProxyRotator, get_proxies
from retailers.amazon import get_amazon_price, AMAZON_ID
from retailers.tradeinn import get_tradeinn_price, TRADEINN_ID


def process_product(db, proxy_rotator, product) -> None:
    retailer_id = str(product["retailer_id"])
    if retailer_id == AMAZON_ID: get_amazon_price(db, proxy_rotator, product)
    elif retailer_id == TRADEINN_ID: get_tradeinn_price(db, proxy_rotator, product)
    else: print(f"Unknown retailer: {product}")


def main() -> None:
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