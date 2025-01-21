from dotenv import load_dotenv
from db import Database, iterate_collection
from proxy_rotator import ProxyRotator, get_proxies
from amazon import get_amazon_html, parse_amazon_product


AMAZON_ID = "678fe61421cc010007e27780"


def main():
    load_dotenv()
 
    db = Database()

    proxies = get_proxies()
    proxy_rotator = ProxyRotator(proxies)

    for product in iterate_collection(db, "monitored"):
        retailer_id = str(product["retailer_id"])
        url = product["url"]
        if retailer_id == AMAZON_ID:
            html = get_amazon_html(proxy_rotator, url)
            product = parse_amazon_product(html)
            print(product)
        else:
            print(f"Unknown retailer: {product}")


if __name__ == "__main__":
    main()