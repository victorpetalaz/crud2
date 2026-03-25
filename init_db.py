import sqlite3

def init_db():
    conn = sqlite3.connect('games.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            plat TEXT NOT NULL,
            yr INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()