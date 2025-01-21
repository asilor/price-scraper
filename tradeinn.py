from proxies import ProxyRotator
from selectolax.parser import HTMLParser


def get_tradeinn_price(proxy_rotator: ProxyRotator, country_id: str, url: str):
    html = proxy_rotator.get_content(url)
    
    tree = HTMLParser(html)

    price_element = tree.css_first("p#js-precio")
    price_text = price_element.text().strip()
    price = float(price_text.split()[0])

    return price