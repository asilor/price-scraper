from database import Database, store_price
from proxies import ProxyRotator
from selectolax.parser import HTMLParser


AMAZON_ID = "678fe61421cc010007e27780"


def get_amazon_price(db: Database, proxy_rotator: ProxyRotator, product: dict) -> None:
    # html = get_amazon_html(proxy_rotator, url)
    # price = parse_amazon_product(html)
    price = 809.33
    return price


def get_amazon_html(proxy_rotator: ProxyRotator, url: str) -> str:
    """Given an Amazon url, return the HTML content."""
    
    while True:
        html = proxy_rotator.get_content(url)
        if "Enter the characters you see below" not in html:
            print(f"{url} Success")
            return html
        else:
            print(f"{url} CAPTCHA")


def parse_amazon_product(html: str) -> str:
    """Given the HTML, return the product information."""

    tree = HTMLParser(html)

    title_element = tree.css_first("h1 span")
    price_symbol_element = tree.css_first("span.a-price-symbol")
    price_whole_element = tree.css_first("span.a-price-whole")
    price_fraction_element = tree.css_first("span.a-price-fraction")

    product_title = title_element.text().strip() if title_element else "Title not found"
    price_symbol = price_symbol_element.text() if price_symbol_element else "Symbol not found"
    price_whole = price_whole_element.text().replace(".", "") if price_whole_element else "Whole part not found"
    price_fraction = price_fraction_element.text() if price_fraction_element else "Fraction not found"

    return f"{product_title} {price_symbol}{price_whole}.{price_fraction}"
