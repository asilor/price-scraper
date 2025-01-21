from dotenv import load_dotenv
from db import Database, iterate_collection
from proxies import ProxyRotator, get_proxies
from amazon import get_amazon_price
from tradeinn import get_tradeinn_price

AMAZON_ID = "678fe61421cc010007e27780"
TRADEINN_ID = "67900fe721cc010007e27784"

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

        print(f"{product_id} {price}") # store in db


if __name__ == "__main__":
    main()