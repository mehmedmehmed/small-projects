import sqlite3

database = 'test.db'

try:
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE [TEST] (
                       column_1 data_type PRIMARY KEY, 
                       column_2 data_type NOT NULL,
                       column_3 data_type DEFAULT 0, 
                       column_4);
                       ''')
        conn.commit()
        pass
except sqlite3.OperationalError as e:
    print('Failed to pen database:', e)