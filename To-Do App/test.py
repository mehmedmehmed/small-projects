import sqlite3

database = 'test.db'

try:
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE Test (
                       column_1 INTEGER, 
                       column_2 TEXT,
                       column_3 TEXT, 
                       column_4 BOOLEAN DEFAULT FALSE);
                       ''')
        conn.commit()
        pass
except sqlite3.OperationalError as e:
    print('Failed to open database:', e)


def add_task(x1, x2, x3):
    try:
        with sqlite3.connect(database) as connect:
            cursor1 = connect.cursor()
            cursor1.execute(f'''INSERT INTO Test (column_1, column_2, column_3)
            VALUES ({x1}, {x2}, {x3});''')
            connect.commit()
            pass
    except sqlite3.OperationalError as oe:
        print('Failed to Integrate:', oe)
