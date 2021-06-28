import pyodbc

database_name = 'acnh_DB'
tbl_name = 'villager'

conn = pyodbc.connect('Driver={SQL Server}; Server=DOMINI-LAPTOP\SQL2019; Database='
                      + database_name + '; Trusted_Connection=yes;')


def load_villagers():
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT villager.id, villager.name, villager.personality, villager.species FROM '
                       + tbl_name + ' AS villager')

        result = []
        header = [i[0] for i in cursor.description]
        data_set = cursor.fetchall()

        for data_row in data_set:
            result.append(dict(zip(header, data_row)))
        return result
    except pyodbc.DatabaseError as err:
        print('DB Error - code={} error={}'.format(err.args[0], err.args[1]))
        raise err
    finally:
        cursor.close()


def load_villager(villager_id):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ' + tbl_name + ' AS villager WHERE villager.id=?', villager_id)

        header = [i[0] for i in cursor.description]
        data = cursor.fetchone()
        if data is None:
            return None

        return dict(zip(header, data))
    except pyodbc.DatabaseError as err:
        print('DB Error - code={} error={}'.format(err.args[0], err.args[1]))
        raise err
    finally:
        cursor.close()


def search_villagers(v_name):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT villager.id, villager.name, villager.personality, villager.species FROM '
                       + tbl_name + ' AS villager WHERE villager.name LIKE ?', '%{0}%'.format(v_name))

        result = []
        header = [i[0] for i in cursor.description]
        data_set = cursor.fetchall()
        for data_row in data_set:
            result.append(dict(zip(header, data_row)))
        return result
    except pyodbc.DatabaseError as err:
        print('DB Error - code={} error={}'.format(err.args[0], err.args[1]))
        raise err
    finally:
        cursor.close()


def add_villagers(table_name, records):
    try:
        cursor = conn.cursor()
        for record in records:
            cursor.execute('INSERT INTO ' + table_name
                           + ' (name, image_url, personality, species, birth_month, birth_date, catchphrase, hobbies) '
                             'values (?, ?, ?, ?, ?, ?, ?, ?)', record)

        cursor.commit()
        return True
    except pyodbc.DatabaseError as err:
        cursor.roleback()
        print('DB Error - code={} error={}'.format(err.args[0], err.args[1]))
        raise err
    finally:
        cursor.close()
