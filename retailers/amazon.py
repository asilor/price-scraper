from database import Database, store_price
from bson.objectid import ObjectId
from proxies import ProxyRotator
from selectolax.parser import HTMLParser


AMAZON_ID = "678fe61421cc010007e27780"


def get_amazon_price(db: Database, proxy_rotator: ProxyRotator, product: dict) -> None:
    """Gets the price of the given product and stores it in the database."""

    url = str(product["url"])
    html = get_amazon_html(proxy_rotator, url)
    price = parse_amazon_price(html)

    region_id = get_region_id(url)

    product["region_id"] = ObjectId(region_id)
    product["retailer_id"] = ObjectId(AMAZON_ID)

    store_price(db, product, price)
    print(f"url: {url}, region_id: {region_id}, price: {price}")


def get_amazon_html(proxy_rotator: ProxyRotator, url: str) -> str:
    """Given an Amazon url, return the HTML content."""
    
    while True:
        html = proxy_rotator.get_content(url)
        if "Enter the characters you see below" not in html:
            print(f"{url} Success")
            return html
        else:
            print(f"{url} CAPTCHA")


def parse_amazon_price(html: str) -> float:
    """Given the Amazon product page HTML, return the price."""

    tree = HTMLParser(html)

    price_whole_element = tree.css_first("span.a-price-whole")
    price_fraction_element = tree.css_first("span.a-price-fraction")

    price_whole = price_whole_element.text().replace(".", "").replace(",", "")
    price_fraction = price_fraction_element.text()

    price = f"{price_whole}.{price_fraction}"

    return float(price)


def get_region_id(url: str) -> str:
    """Returns the region_id given the url."""

    domain_to_region_id = {
        "amazon.es": "67942b3721cc010007e278df",
        "amazon.it": "679404a321cc010007e2784d",
        "amazon.fr": "6794031521cc010007e2780f",
    }

    for domain, region_id in domain_to_region_id.items():
        if domain in url:
            return region_id

    return None
