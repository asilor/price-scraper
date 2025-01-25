from database import Database, store_price
from bson.objectid import ObjectId
from proxies import ProxyRotator
import json


TRADEINN_ID = "67900fe721cc010007e27784"


def get_tradeinn_prices(db: Database, proxy_rotator: ProxyRotator, product: dict) -> None:
    """Gets the prices of the given product in all available languages and stores it in the database."""

    product["retailer_id"] = ObjectId(TRADEINN_ID)
    
    url = product["url"]
    id_modelo = url.split("/")[-2]

    url_elastic_dc = f"https://dc.tradeinn.com/{id_modelo}"

    headers = {
        'referer': 'https://www.tradeinn.com/'
    }
    
    response = proxy_rotator.get_content(url_elastic_dc, headers=headers)
    product_json = json.loads(response)
    
    precio_paises = product_json["_source"]["productes"][0]["sellers"][0]["precios_paises"]
    
    for precio_pais in precio_paises:
        region_id = get_region_id(precio_pais["id_pais"])
        if region_id:
            price = precio_pais["precio"]

            product["region_id"] = ObjectId(region_id)

            store_price(db, product, price)
            print(f"url: {url}, region_id: {region_id}, price: {price}")


def get_region_id(id_pais: str) -> int:
    """Returns the region_id given the id_pais."""

    id_pais_to_region_id = {
        1: "6793e36a21cc010007e27798",
        2: "6793e38d21cc010007e2779a",
        4: "6793e3a821cc010007e2779c",
        5: "6793e3be21cc010007e2779e",
        8: "6793e41021cc010007e277a0",
        9: "6793e44621cc010007e277a2",
        11: "6793e45d21cc010007e277a4",
        12: "6793e48621cc010007e277a6",
        13: "6793e49821cc010007e277a8",
        14: "6793e4a821cc010007e277aa",
        16: "6793e4ba21cc010007e277ac",
        17: "6793eaca21cc010007e277ae",
        18: "6793ee3f21cc010007e277b0",
        19: "6793ee8421cc010007e277b2",
        21: "6793eeae21cc010007e277b4",
        24: "6793eedf21cc010007e277b6",
        26: "6793eefe21cc010007e277b8",
        27: "6793ef8d21cc010007e277bb",
        28: "6793efa121cc010007e277bd",
        29: "6793efb721cc010007e277bf",
        30: "6793efce21cc010007e277c1",
        31: "6793efe121cc010007e277c3",
        32: "6793f00321cc010007e277c5",
        33: "6793f02221cc010007e277c7",
        34: "6793f03521cc010007e277c9",
        35: "6793f04b21cc010007e277cb",
        37: "6793f06621cc010007e277cd",
        38: "6793f08121cc010007e277cf",
        39: "6793f09921cc010007e277d1",
        40: "6793f0fe21cc010007e277d3",
        41: "6793f13b21cc010007e277d5",
        42: "6793f15821cc010007e277d7",
        43: "6793f18321cc010007e277d9",
        44: "6793f1a321cc010007e277db",
        45: "6793f1b721cc010007e277dd",
        46: "6793f1ec21cc010007e277df",
        47: "6793f20621cc010007e277e1",
        48: "6793f21821cc010007e277e3",
        49: "6793f23b21cc010007e277e5",
        50: "6793f32221cc010007e277e7",
        51: "6793f33e21cc010007e277e9",
        52: "6793f3df21cc010007e277eb",
        53: "6793f40621cc010007e277ed",
        54: "6793f43521cc010007e277ef",
        55: "6793f44621cc010007e277f1",
        56: "6793f45c21cc010007e277f3",
        57: "6793f47621cc010007e277f5",
        58: "6793f48a21cc010007e277f7",
        59: "6793f50e21cc010007e277f9",
        60: "6793f53321cc010007e277fb",
        61: "6793f54a21cc010007e277fd",
        62: "6793f55e21cc010007e277ff",
        63: "6793f57321cc010007e27801",
        64: "6793f59c21cc010007e27803",
        65: "6793f5a421cc010007e27805",
        66: "6794025221cc010007e27807",
        67: "679402fa21cc010007e27809",
        68: "6794030021cc010007e2780b",
        69: "6794030921cc010007e2780d",
        70: "6794031521cc010007e2780f", 
        71: "6794034f21cc010007e2781b",
        72: "6794035c21cc010007e2781d",
        73: "6794036421cc010007e2781f",
        74: "679403fb21cc010007e27821",
        75: "6794040221cc010007e27823",        
        76: "6794040921cc010007e27825",
        77: "6794041021cc010007e27827",
        78: "6794041921cc010007e27829",
        79: "6794042221cc010007e2782b",
        80: "6794042821cc010007e2782d",
        82: "6794042e21cc010007e2782f",
        83: "6794043621cc010007e27831",
        85: "6794043d21cc010007e27833",
        86: "6794044921cc010007e27835",
        87: "6794045221cc010007e27837",
        88: "6794045921cc010007e27839",
        89: "6794046021cc010007e2783b",
        90: "6794046821cc010007e2783d",
        91: "6794046f21cc010007e2783f",
        92: "6794047621cc010007e27841",
        93: "6794047d21cc010007e27843",
        94: "6794048421cc010007e27845",
        95: "6794049221cc010007e27847",
        96: "6794049521cc010007e27849",
        97: "6794049d21cc010007e2784b",
        98: "679404a321cc010007e2784d",
        99: "6794110c21cc010007e2784f",
        100: "6794111321cc010007e27851",
        102: "6794111a21cc010007e27853",
        103: "6794112121cc010007e27855",
        104: "6794112821cc010007e27857",
        105: "6794112f21cc010007e27859",
        107: "6794113521cc010007e2785b",
        108: "6794113b21cc010007e2785d",
        109: "6794114121cc010007e2785f",
        110: "6794114821cc010007e27861",
        111: "6794115021cc010007e27863",
        112: "6794115621cc010007e27865",
        113: "6794115d21cc010007e27867",
        114: "6794116421cc010007e27869",
        115: "6794116b21cc010007e2786b",
        116: "6794117121cc010007e2786d",
        117: "6794117721cc010007e2786f",
        118: "6794117f21cc010007e27871",
        120: "67941f3621cc010007e2788b",
        121: "6794118621cc010007e27873",
        122: "6794118e21cc010007e27875",
        123: "6794119421cc010007e27877",
        124: "6794119a21cc010007e27879",
        125: "679411a121cc010007e2787b",
        126: "679411aa21cc010007e2787d",
        127: "679411b221cc010007e2787f",
        129: "679411bb21cc010007e27881",
        130: "679411c221cc010007e27883",
        131: "679411cc21cc010007e27885",
        132: "679411d321cc010007e27887",
        133: "679411da21cc010007e27889",
        134: "6794219621cc010007e2788d",
        135: "6794219e21cc010007e2788f",
        136: "679421a421cc010007e27891",
        137: "679421ab21cc010007e27893",
        138: "679421b221cc010007e27895",
        139: "679421ba21cc010007e27897",
        140: "679421c121cc010007e27899",
        141: "679421c721cc010007e2789b",
        142: "679421cf21cc010007e2789d",
        145: "679421db21cc010007e2789f",
        147: "679421e421cc010007e278a1",
        148: "679421f221cc010007e278a3",
        150: "679421f921cc010007e278a5",
        151: "6794220021cc010007e278a7",
        152: "6794220721cc010007e278a9",
        153: "6794220d21cc010007e278ab",
        154: "6794221421cc010007e278ad",
        155: "6794221b21cc010007e278af",
        156: "6794222121cc010007e278b1",
        157: "6794222a21cc010007e278b3",
        158: "6794223021cc010007e278b5",
        159: "6794223621cc010007e278b7",
        160: "6794223d21cc010007e278b9",
        161: "6794224421cc010007e278bb",
        163: "6794224c21cc010007e278bd",
        164: "6794225421cc010007e278bf",
        165: "6794225a21cc010007e278c1",
        167: "6794226221cc010007e278c3",
        175: "67942b1c21cc010007e278d7",
        180: "67942b3721cc010007e278df",
        192: "67942b6121cc010007e278eb",
        209: "67942fa921cc010007e2790b",
        210: "67942faf21cc010007e2790d",
    }

    region_id = id_pais_to_region_id.get(id_pais, None)
    
    return region_id
