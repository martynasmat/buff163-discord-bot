from add_queries import open_connection
import urllib.request
import json
import statistics


URL = 'https://buff.163.com/api/market/goods/sell_order?game=csgo'


class Item:
    def __init__(self, json_data, purchase_url):
        self.json_data = json_data
        self.purchase_url = purchase_url
        self.price_list = []

    def assign_price_list(self, items):
        for item_element in items:
            self.price_list.append(float(item_element["price"]))


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
    entry = ('http://customer-%s:%s@pr.oxylabs.io:7777' %
             (username, password))
    query = urllib.request.ProxyHandler({
        'http': entry,
        'https': entry,
    })

    req_url = f"{URL}&goods_id={item_param[2]}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1"

    for _ in range(0, 20):
        try:
            execute = urllib.request.build_opener(query)
            response = execute.open(req_url).read()
            json_data = json.loads(response)
            item_obj = Item(json_data, req_url)
            return item_obj
        except:
            pass


def is_deal_found(item_obj_param, item_tracker_param):
    desired_float = item_tracker_param[4]
    desired_pattern_id = item_tracker_param[5]
    desired_margin = item_tracker_param[6]
    median = statistics.median(item_obj_param.price_list)
    found_deal = False
    for i in range(0, 5):
        print(median)
        print(100 - item_obj_param.price_list[i] / median * 100)
        if 100 - item_obj_param.price_list[i] / median * 100 >= desired_margin:
            found_deal = True
            break

    return found_deal


def deal_found(item_obj_param):
    pass


for item_tracker in get_all_items_from_db():
    item_obj = send_request(item_tracker)
    item_obj.assign_price_list(item_obj.json_data["data"]["items"])
    if is_deal_found(item_obj, item_tracker):
        deal_found(item_obj)

    print(item_obj.price_list)
