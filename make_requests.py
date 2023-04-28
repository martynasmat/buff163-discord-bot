import requests
from add_queries import open_connection


def get_all_items():
    connection = open_connection()
    cursor = connection.cursor()
    query = """SELECT * FROM buff_tracker"""
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results


def exec_requests(items):
    return


print(get_all_items())