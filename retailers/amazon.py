from database import Database, store_price
from bson.objectid import ObjectId
from proxies import ProxyRotator
from selectolax.parser import HTMLParser


AMAZON_ID = "678fe61421cc010007e27780"


def get_amazon_price(db: Database, proxy_rotator: ProxyRotator, product: dict) -> None:
    """Gets the price of the given product and stores it in the database."""

    """
    There are 3 necessary cookies to preserve the country throught requests 
    (even if the ip changes to another country in subsequent requests):
    sesion-id, session-id-time, ubid-acbde
    """

    cookies = {
        "i18n-prefs": "",
        "session-id": "",
        "session-id-time": "",
        "session-token": "",
        "ubid-acbde": ""
    }

    url = str(product["url"])
    html = proxy_rotator.get_content(url, cookies=cookies)

    with open("index.html", "w") as f:
        f.write(html)

    price = parse_amazon_price(html)

    region_id = get_region_id(url)
 
    product["region_id"] = ObjectId(region_id)
    product["retailer_id"] = ObjectId(AMAZON_ID)

    #store_price(db, product, price)
    print(f"url: {url}, region_id: {region_id}, price: {price}")


def get_amazon_html(proxy_rotator: ProxyRotator, url: str) -> str:
    """Given an Amazon url, return the HTML content."""
    
    while True:
        html = proxy_rotator.get_content(url)
        if "Enter the characters you see below" not in html:
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
        "amazon.com.au": "6793e45d21cc010007e277a4",  # Australia
        "amazon.com.be": "6793ee8421cc010007e277b2",  # Belgium
        "amazon.com.br": "6793efa121cc010007e277bd",  # Brazil
        "amazon.ca": " 6793f04b21cc010007e277cb",     # Canada
        "amazon.cn": "6793f15821cc010007e277d7",      # China
        "amazon.eg": "6793f53321cc010007e277fb",      # Egypt
        "amazon.fr": "6794031521cc010007e2780f",      # France
        "amazon.de": "6794040221cc010007e27823",      # Germany
        "amazon.in": "6794047d21cc010007e27843",      # India
        "amazon.it": "679404a321cc010007e2784d",      # Italy
        "amazon.co.jp": "794111321cc010007e27851",    # Japan
        "amazon.com.mx": "6794111321cc010007e27851",  # Mexico
        "amazon.nl": "679421cf21cc010007e2789d",      # Netherlands
        "amazon.pl": "6794223021cc010007e278b5",      # Poland
        "amazon.sa": "67942aeb21cc010007e278c9",      # Saudi Arabia
        "amazon.sg": "67942b0e21cc010007e278d3",      # Singapore
        "amazon.es": "67942b3721cc010007e278df",      # Spain
        "amazon.se": "67942b5b21cc010007e278e9",      # Sweden
        "amazon.com.tr": "67942f6c21cc010007e278ff",  # Turkey
        "amazon.ae": "67942f8d21cc010007e27909",      # United Arab Emirates
        "amazon.co.uk": "67942fa921cc010007e2790b",   # United Kingdom
        "amazon.com": "67942faf21cc010007e2790d"      # United States
    }

    for domain, region_id in domain_to_region_id.items():
        if domain in url:
            return region_id

    return None
