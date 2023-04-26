from thefuzz import process
import mysql.connector

def read_ids():
    with open('skin_id_list.txt', 'r', encoding="utf-8") as id_file:
        return id_file.readlines()


def get_ids():
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


# def add_tracker(name_to_search, float_param, pattern_id_param, discord_id):
#     skin_info = search(name_to_search)
#     connection = sqlite3.connect('user_db.db')
#     cursor = connection.cursor()
#     cursor.execute(f"""
#     INSERT INTO tracker VALUES 
#     ('{skin_info[0]}', '{skin_info[1]}', {float_param}, '{pattern_id_param}', '{discord_id}')
#     """)
#     connection.commit()

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

        query += f"""('{value[0]}', '{value[1]}', '{key}'), """

    query = query[:len(query) - 2]
    query += ';'
    cursor = db.cursor()
    cursor.execute(query)

    db.commit()
    db.close()
