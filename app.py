from flask import Flask, jsonify
import pyodbc

app = Flask(__name__)


def get_villagers(json_str=False):

    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DOMINI-LAPTOP\SQL2019;'
                          'Database=acnh_DB;'
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM acnh_DB.DBO.villagers')

    data_json = []
    header = [i[0] for i in cursor.description]
    data = cursor.fetchall()
    for i in data:
        print(i)
        print(type(i))
        data_json.append(dict(zip(header, i)))
    return (data_json)

@app.route('/villager', methods=['GET'])
def villagers():
    villagers_list = get_villagers()
    print(villagers_list)
    print(type(villagers_list))
    return jsonify(villagers_list), 200
