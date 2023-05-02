from add_queries import open_connection
import urllib3
import json
import statistics
import math
import currency_converter as cc
from webhook import construct_json, notify_user


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


def get_all_items_from_db():
    connection = open_connection()
    cursor = connection.cursor()
    query = """SELECT * FROM buff_tracker"""
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results


def send_request(item_param):
    username = 'buffbot'
    password = 'bUffbot123123987987'
    proxy_login_headers = urllib3.make_headers(proxy_basic_auth=f'{username}:{password}')
    entry = ('http://customer-%s:%s@pr.oxylabs.io:7777' %
             (username, password))
    query = urllib3.ProxyManager(entry, proxy_headers=proxy_login_headers)

    req_url = f"{URL}&goods_id={item_param[2]}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&_=1682875931788"

    for _ in range(0, 20):
        try:
            response = query.request('GET', req_url)
            print(json.loads(response.data)["data"]["items"][0])
            json_data = json.loads(response.data)
            item_obj = Item(json_data, f"https://buff.163.com/goods/{item_param[2]}#tab=selling", item_param[0])
            return item_obj
        except:
            pass


def is_deal_found(item_obj_param, item_tracker_param):
    desired_float = item_tracker_param[4]
    desired_pattern_id = item_tracker_param[5]
    desired_margin = item_tracker_param[6]
    median = statistics.median(item_obj_param.price_list)
    found_deal = False
    deal_obj = ''
    for i in range(0, math.floor(len(item_obj_param.price_list) / 2)):
        print(median)
        print(100 - item_obj_param.price_list[i] / median * 100)
        if 100 - item_obj_param.price_list[i] / median * 100 >= desired_margin:
            found_deal = True
            deal_obj = Deal(
                            float(item_obj_param.json_data["data"]["items"][i]["price"]),
                            item_obj_param.purchase_url,
                            item_obj_param.item_name,
                            item_obj_param.json_data["data"]["items"][i]["asset_info"]["paintwear"],
                            item_obj_param.json_data["data"]["items"][i]["asset_info"]["info"]["paintseed"],
                            median,
                            item_obj_param.json_data["data"]["items"][i]["img_src"],
                            item_tracker_param[3]
                            )
            break
    return found_deal, deal_obj


for item_tracker in get_all_items_from_db():
    item_obj = send_request(item_tracker)
    item_obj.assign_price_list(item_obj.json_data["data"]["items"])
    print(item_obj)
    find_deal = is_deal_found(item_obj, item_tracker)
    if find_deal[0]:
        deal_object = find_deal[1]
        json_data = construct_json(deal_object)
        notify_user(json_data)

    print(item_obj.price_list)
