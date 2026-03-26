import sqlite3

def exec_q(q, *args, fetch=False, commit=False):
    conn = sqlite3.connect('games.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    res = None
    
    try:
        c.execute(q, args)
        if commit:
            conn.commit()
            res = c.rowcount 
        if fetch:
            res = c.fetchall()
    finally:
        conn.close()
    
    return res

def init_db():
    conn = sqlite3.connect('games.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            platform TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
