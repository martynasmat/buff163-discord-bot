from thefuzz import process
import mysql.connector

def read_ids():
    with open('skin_id_list.txt', 'r', encoding="utf-8") as id_file:
        return id_file.readlines()


def get_ids():
    # id_dict stores all skin names as keys and a list containing their
    # respective formatted names and buff.163.com ids as values
    id_dict = dict()

    lines = read_ids()
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


def search(name_param):
    id_dictionary = get_ids()
    return id_dictionary[process.extractOne(name_param, list(id_dictionary.keys()))[0]]


def insert_buff_items_to_db():
    db = mysql.connector.connect(
        host='containers-us-west-41.railway.app',
        user='root',
        password='5bH078yqN9J3m4JNMlal',
        database='railway',
        port='6011'
    )

    item_ids = get_ids()

    query = f"""INSERT INTO buff_items VALUES """

    for key, value in item_ids.items():
        value[1] = value[1].replace("'", "''")
        key = key.replace("'", "''")
        
        # ('goods_id', 'item_name', 'item_name_formatted')
        query += f"""('{value[0]}', '{value[1]}', '{key}'), """

    query = query[:len(query) - 2]  # Remove trailing comma and space
    query += ';'                    # Query end
    db.cursor().execute(query)

    db.commit()
    db.close()


def query_item_by_name(item_name):
    db = mysql.connector.connect(
        host='containers-us-west-41.railway.app',
        user='root',
        password='5bH078yqN9J3m4JNMlal',
        database='railway',
        port='6011'
    )

    query = f"""SELECT * FROM buff_items WHERE goods_id={search(item_name)[0]};"""
    cursor = db.cursor()
    cursor.execute(query)

    result = cursor.fetchone()  # Result of query
    db.close()
    
    return result

print(query_item_by_name("aquamarine"))