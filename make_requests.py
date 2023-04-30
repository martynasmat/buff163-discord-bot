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
            self.price_list.append(item_element["price"])


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


for item in get_all_items_from_db():
    item_obj = send_request(item)
    item_obj.assign_price_list(item_obj.json_data["data"]["items"])

    print(item_obj.price_list)
