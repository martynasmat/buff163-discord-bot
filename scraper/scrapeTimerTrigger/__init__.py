import azure.functions as func
import mysql.connector
import datetime
import logging
import os
#from dotenv import load_dotenv
#load_dotenv()

from scrapeTimerTrigger.make_requests import send_request, get_all_items_from_db, is_deal_found
from scrapeTimerTrigger.webhook import construct_json, notify_user
from scrapeTimerTrigger.make_requests import Item


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    logging.info('-----------------------------------------------------------')
    logging.info('Connecting to DB')

    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

    logging.info('Connected to DB')

    items = get_all_items_from_db(connection)

    logging.info("LOOP START")
    logging.info(f"ITEMS: {items}")

    for item_tracker in items:
        logging.info("LOOPING")
        logging.info(f"ITEM: {item_tracker}")
        
        item_obj = send_request(item_tracker)
        item_obj.assign_price_list(item_obj.json_data["data"]["items"])

        logging.info("****************************************")

        find_deal = is_deal_found(item_obj, item_tracker)
        if find_deal[0]:
            deal_object = find_deal[1]
            json_data = construct_json(deal_object)
            notify_user(json_data)

    logging.info("LOOP END")

    connection.close()


# UseDevelopmentStorage=true