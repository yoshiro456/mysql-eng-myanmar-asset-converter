import json
import json
from msilib.schema import Error
import mysql.connector
from utils.rabbit import Rabbit


def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            database="myanmar_dictionary",
            user="root",
            password=""
        )
    except Error as e:
        print(e)


def query_find_all(cursor, table):
    cursor.execute(
        'SELECT `Word`, `state`, `def` FROM {t} LIMIT 10'.format(t=table))


def write_to_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)


def eng_to_mym_convert():
    connection = get_connection()
    cursor = connection.cursor()
    query_find_all(cursor, 'mydblist')

    result = cursor.fetchall()

    eng_mym_dict = {}
    for i in result:
        word = i[0]
        state = i[1]
        content = Rabbit.zg2uni(i[2]).replace('|', '')

        if (word in eng_mym_dict):
            eng_mym_dict[word] += '\n({x}) {y}'.format(x=state, y=content)
        else:
            eng_mym_dict[word] = '({x}) {y}'.format(x=state, y=content)

    return eng_mym_dict


def mym_to_eng_convert():
    connection = get_connection()
    cursor = connection.cursor()
    query_find_all(cursor, 'myen')

    result = cursor.fetchall()

    mym_eng_dict = {}
    for i in result:
        word = Rabbit.zg2uni(i[0]).replace('|', '')
        state = i[1]
        content = i[2]

        if (word in mym_eng_dict):
            mym_eng_dict[word] += '\n({x}) {y}'.format(x=state, y=content)
        else:
            mym_eng_dict[word] = '({x}) {y}'.format(x=state, y=content)

    return mym_eng_dict


def combine_both(eng_to_mym, mym_to_eng):
    all_dict = []
    count = 1

    for key, value in eng_to_mym.items():
        all_dict.append({'id': count, 'word': key, 'content': value})
        count += 1

    for key, value in mym_to_eng.items():
        all_dict.append({'id': count, 'word': key, 'content': value})
        count += 1

    return all_dict


eng_to_mym = eng_to_mym_convert()
mym_to_eng = mym_to_eng_convert()
all_dict = combine_both(eng_to_mym, mym_to_eng)

write_to_file('dist/eng_to_mym.json', json.dumps(eng_to_mym))
write_to_file('dist/mym_to_eng.json', json.dumps(mym_to_eng))
write_to_file('dist/all.json', json.dumps(all_dict))
