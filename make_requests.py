from add_queries import open_connection
import urllib.request
import json


URL = 'https://buff.163.com/api/market/goods/sell_order?game=csgo'


def get_all_items_from_db():
    connection = open_connection()
    cursor = connection.cursor()
    query = """SELECT * FROM buff_tracker"""
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results


def send_request(item_goods_id):
    username = 'buffbot'
    password = 'bUffbot123123987987'
    entry = ('http://customer-%s:%s@pr.oxylabs.io:7777' %
             (username, password))
    query = urllib.request.ProxyHandler({
        'http': entry,
        'https': entry,
    })
    execute = urllib.request.build_opener(query)
    return json.loads(execute.open(f"{URL}&goods_id={item_goods_id}").read())["data"]["items"]


def process_data(item_json):
    price_list = list()
    for item_data in item_json:
        price_list.append(item_data["price"])

    return price_list


for item in get_all_items_from_db():
    print(process_data(send_request(item[2])))
