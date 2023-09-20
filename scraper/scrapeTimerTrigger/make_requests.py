import statistics
import math
import currency_converter as cc
from scrapeTimerTrigger.webhook import construct_json, notify_user
from scrapeTimerTrigger.get_proxies import get_proxy
import logging
import requests

URL = 'https://buff.163.com/api/market/goods/sell_order?game=csgo'

class Item:
    def __init__(self, json_data, purchase_url, name):
        self.json_data = json_data
        self.purchase_url = purchase_url
        self.price_list = []
        self.item_name = name

    def assign_price_list(self, items):
        for item_element in items:
            self.price_list.append(float(item_element["price"]))


class Deal:
    def __init__(self, listing_price_cny, purchase_url, name, float_val, pattern_id, median_price, screenshot_url, discord_id):
        self.listing_price_cny = listing_price_cny
        self.purchase_url = purchase_url
        self.name = name
        self.float_val = float_val
        self.pattern_id = pattern_id
        self.median_price = median_price
        self.listing_price_eur = cc.CurrencyConverter().convert(listing_price_cny, 'CNY', 'EUR')
        self.screenshot_url = screenshot_url
        self.discord_id = discord_id


def get_all_items_from_db(connection):
    cursor = connection.cursor()
    query = """SELECT * FROM buff_tracker;"""
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

def send_request(item_param):
    proxy_login = get_proxy()
    req_url = f"{URL}&goods_id={item_param[3]}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_=1682875931788"

    logging.info(proxy_login)

    try:
        response = requests.get(url=req_url,
                                proxies={
                                    "http": f"http://{proxy_login[2]}:{proxy_login[3]}@{proxy_login[0]}:{proxy_login[1]}/",
                                    "https": f"http://{proxy_login[2]}:{proxy_login[3]}@{proxy_login[0]}:{proxy_login[1]}",
                                })

        logging.info(response)

        json_data = response.json()
        item_obj = Item(json_data, f"https://buff.163.com/goods/{item_param[3]}#tab=selling", item_param[1])
        return item_obj
    except:
        logging.info("ERROR FETCHING DATA")
        pass


def is_deal_found(item_obj_param, item_tracker_param):
    desired_float = item_tracker_param[5]
    desired_pattern_id = item_tracker_param[6]
    desired_margin = item_tracker_param[7]
    median = statistics.median(item_obj_param.price_list)
    found_deal = False
    deal_obj = ''
    for i in range(0, math.floor(len(item_obj_param.price_list) / 2)):
        
        logging.info(f"Median: {median}")
        logging.info(f"""Price: {item_obj_param.json_data["data"]["items"][i]["price"]}""")
        logging.info(f"Margin: {100 - item_obj_param.price_list[i] / median * 100}")
        
        if 100 - item_obj_param.price_list[i] / median * 100 >= int(desired_margin):
            found_deal = True
            deal_obj = Deal(
                            float(item_obj_param.json_data["data"]["items"][i]["price"]),
                            item_obj_param.purchase_url,
                            item_obj_param.item_name,
                            item_obj_param.json_data["data"]["items"][i]["asset_info"]["paintwear"],
                            item_obj_param.json_data["data"]["items"][i]["asset_info"]["info"]["paintseed"],
                            median,
                            item_obj_param.json_data["data"]["items"][i]["img_src"],
                            item_tracker_param[4]
                            )
            break
    return found_deal, deal_obj




