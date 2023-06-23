import sqlite3
import datetime


def new_base():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS currency_rate(
        Digital_code INT,
        Letter_code TEXT,
        Units INT,
        Currency TEXT,
        Course REAL);
        ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS percentages(
    Date TEXT);
    ''')
    cur.close()


def new_data(result: tuple):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    for data in result:
        if data[-2] == 'СДР (специальные права заимствования)':
            name = 'СДР'
        else:
            name = data[-2]
        cur.execute(f'ALTER TABLE percentages ADD {name} REAL')
        cur.execute('INSERT INTO currency_rate VALUES(?,?,?,?,?);', data)
    conn.commit()
    cur.close()


def updating_data(result: tuple):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    sqlite_update_query = 'UPDATE currency_rate SET Course=? WHERE Currency=?'
    for data in result:
        update = (data[-2:][::-1],)
        cur.executemany(sqlite_update_query, update)
    conn.commit()
    cur.close()


def difference(result: tuple):
    percent_of_changes = []

    year = str(datetime.date.today().year)
    add_time = str(datetime.date.today()).replace(f'{year}-', '')
    percent_of_changes.append(add_time)

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    sql_select_query = 'SELECT * FROM currency_rate WHERE Digital_code=?'
    for data in result:
        cur.execute(sql_select_query, (data[0],))
        records = cur.fetchall()
        if int(data[0]) == int(records[0][0]):
            print(f'{data[-2]}: there are no changes')
            percent_of_changes.append(0)
        else:
            number_records = float(records[0][-1].replace(',', '.'))
            number_site = float(data[-1].replace(',', '.'))
            changes = (number_site - number_records) / number_records * 100.0
            percent_of_changes.append(f'{changes:.3f}')
            print(f'{data[-2]}: changes to {changes:.3f}%')
    cur.execute(
        'INSERT INTO percentages VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);',
        tuple(percent_of_changes))
    conn.commit()
    cur.close()
