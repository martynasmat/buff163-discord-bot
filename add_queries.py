import mysql.connector
import difflib


def open_connection():
    return mysql.connector.connect(
        host='containers-us-west-41.railway.app',
        user='root',
        password='5bH078yqN9J3m4JNMlal',
        database='railway',
        port='6011'
    )


#  def read_ids():
#      with open('skin_id_list.txt', 'r', encoding="utf-8") as id_file:
#          return id_file.readlines()


def fetch_ids():
    connection = open_connection()
    cursor = connection.cursor()

    query = """SELECT item_name_formatted FROM buff_items"""
    cursor.execute(query)
    result = cursor.fetchall()

    connection.close()
    return [x[0] for x in result]


def get_ids():
    # id_dict stores all skin names as keys and a list containing their
    # respective formatted names and buff.163.com ids as values
    id_dict = dict()

    lines = fetch_ids()
    for line in lines:
        line = line.split(';')
        line_formatted = line[1].lower()
        line_formatted = line_formatted.replace('★', '')
        line_formatted = line_formatted.strip()
        line_formatted = line_formatted.replace('\n', '')
        line_formatted = line_formatted.replace('| ', '')
        line_formatted = line_formatted.replace('(', '')
        line_formatted = line_formatted.replace(')', '')
        id_dict[line_formatted] = [line[0], line[1].replace('\n', '')]

    return id_dict


def search_by_name(name_param):
    all_names = fetch_ids()
    max_names = list()

    for name in all_names:
        max_names.append((name, difflib.SequenceMatcher(None, name, name_param).ratio()))

    return sorted(max_names, key=lambda item: item[1], reverse=True)[0][0]


def insert_buff_items_to_db():
    connection = open_connection()
    item_ids = get_ids()

    query = f"""INSERT INTO buff_items VALUES """

    for key, value in item_ids.items():
        value[1] = value[1].replace("'", "''")
        key = key.replace("'", "''")
        
        # ('goods_id', 'item_name', 'item_name_formatted')
        query += f"""('{value[0]}', '{value[1]}', '{key}'), """

    query = query[:len(query) - 2]  # Remove trailing comma and space
    query += ';'                    # Query end
    connection.cursor().execute(query)

    connection.commit()
    connection.close()


def query_item_by_name(item_name):
    connection = open_connection()

    query = f"""SELECT * FROM buff_items WHERE item_name_formatted='{search_by_name(item_name)}';"""
    cursor = connection.cursor()
    cursor.execute(query)

    result = cursor.fetchone()  # Result of query
    connection.close()
    
    return result


def query_item_by_id(id_param):
    connection = open_connection()

    query = f"""SELECT * FROM buff_items WHERE goods_id='{id_param}';"""
    cursor = connection.cursor()
    cursor.execute(query)

    result = cursor.fetchone()  # Result of query
    connection.close()

    return result


print(query_item_by_name(input()))
