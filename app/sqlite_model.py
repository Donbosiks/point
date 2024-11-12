import sqlite3

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS classes 
                        (id INTEGER PRIMARY KEY, name TEXT, points FLOAT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS explanations
                        (id INTEGER PRIMARY KEY, item_name TEXT, explanation TEXT, points FLOAT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS criteria
                        (id INTEGER PRIMARY KEY, criteria_user TEXT)''')
        conn.commit()