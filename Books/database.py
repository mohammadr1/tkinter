import sqlite3

class BookDAO:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                price INTEGER,
                stock INTEGER
            )
        ''')
        self.conn.commit()

    def insert_book(self, title, author, price, stock):
        self.cursor.execute('INSERT INTO books (title, author, price, stock) VALUES (?, ?, ?, ?)', (title, author, price, stock))
        self.conn.commit()

    def get_all_books(self):
        self.cursor.execute('SELECT * FROM books')
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()