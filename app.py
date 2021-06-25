from flask import Flask, jsonify
import pyodbc

app = Flask(__name__)


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DOMINI-LAPTOP\SQL2019;'
                      'Database=acnh_DB;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()


def get_villagers():

    # conn = pyodbc.connect('Driver={SQL Server};'
    #                       'Server=DOMINI-LAPTOP\SQL2019;'
    #                       'Database=acnh_DB;'
    #                       'Trusted_Connection=yes;')
    #
    # cursor = conn.cursor()
    cursor.execute('SELECT * FROM villagers')

    data_json = []
    header = [i[0] for i in cursor.description]
    data = cursor.fetchall()

    for i in data:
        data_json.append(dict(zip(header, i)))
    return (data_json)


def get_villager(id):

    cursor.execute('SELECT * FROM villagers where villagers.id=?', id)

    header = [i[0] for i in cursor.description]
    data = cursor.fetchone()
    if data is None:
        return None

    return dict(zip(header, data))


def search_villagers(v_name):

    cursor.execute('SELECT * from villagers WHERE villagers.name like ?', '%{0}%'.format(v_name))

    data_json = []
    header = [i[0] for i in cursor.description]
    data = cursor.fetchall()
    for i in data:
        data_json.append(dict(zip(header, i)))
    print(data_json)
    return (data_json)

    # all in the search box will return all the tuples
    # if len(data) == 0 and v_name == 'all':
    #     cursor.execute('SELECT villagers.name, villagers.personlity  from villagers')


@app.route('/villager', methods=['GET'])
def villagers():
    villagers_list = get_villagers()
    return jsonify(villagers_list), 200


@app.route('/villager/<int:id>', methods=['GET'])
def villager(id):
    result = get_villager(id)

    if result is None:
        return jsonify({'id': id, 'error': 'Villager does not exist'}), 404
    else:
        return jsonify(result), 200


@app.route('/search/<string:v_name>', methods=['GET'])
def search(v_name):
    result = search_villagers(v_name)
    # if result is None:
    #     return jsonify({'v_name': id, 'error': 'No villagers'}), 404
    # else:
    return jsonify(result), 200
