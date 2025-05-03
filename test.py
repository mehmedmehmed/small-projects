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
    print('Failed to pen database:', e)