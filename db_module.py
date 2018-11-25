import random
import string
import sqlite3
from generate_data import generateTable




def main():
    table_name='USER_DATA'
    db_name='example.db'
    res=create_and_fill_db(table_name, db_name)
    #print(select_data(table_name, db_name))
    print(res)

def select_data(table_name=None, db_name=None):
    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    c=conn.cursor()
    c.execute('select {} from {}'.format('first_name', table_name))
    result=c.fetchall()
    return result


def create_and_fill_db(table_name=None, db_name=None):
    my_gen = generateTable()
    data = my_gen.generateTable(100)
    columns = my_gen.columns.keys()
    fields = ''.join([i + ' VARCHAR(255),' for i in columns])[0:-1]

    drop_command = 'DROP TABLE {}'.format(table_name)
    create_command = 'CREATE TABLE IF NOT EXISTS {}({})'.format(table_name, fields)
    ins_command = 'INSERT INTO {} VALUES (?,?,?,?,?,?)'.format(table_name)

    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(drop_command)
    c.execute(create_command)
    converted_data = (tuple(i.values()) for i in data)
    c.executemany(ins_command, converted_data)
    c.execute('SELECT * FROM {}'.format(table_name))
    result = c.fetchall()
    return result


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

if __name__ == '__main__':
    main()