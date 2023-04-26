from thefuzz import process
import sqlite3
import mysql.connector

def read_ids():
    with open('skin_id_list.txt', 'r', encoding="utf-8") as id_file:
        return id_file.readlines()


def get_ids():
    # id_dict stores all skin names as keys and a list containing their
    # respective formatted names and buff.163.com ids as values
    id_dict = dict()

    # name_list contains all formatted names of skins
    name_list = list()

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
        name_list.append(line_formatted)

    return id_dict, name_list


def search(name_param):
    id_dictionary, all_names = get_ids()
    return id_dictionary[process.extractOne(name_param, all_names)[0]]


def add_tracker(name_to_search, float_param, pattern_id_param, discord_id):
    skin_info = search(name_to_search)
    connection = sqlite3.connect('user_db.db')
    cursor = connection.cursor()
    cursor.execute(f"""
    INSERT INTO tracker VALUES 
    ('{skin_info[0]}', '{skin_info[1]}', {float_param}, '{pattern_id_param}', '{discord_id}')
    """)
    connection.commit()

def connect_to_database():
    db = mysql.connector.connect(
        host='containers-us-west-41.railway.app',
        user='root',
        password='5bH078yqN9J3m4JNMlal',
        database='railway',
        port='6011'
    )

connect_to_database()