import sqlite3

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("expenses.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, day date, amount integer, category text, notes text)")
        self.conn.commit()

    def add_entry(self, date, amount, category, notes):
        self.cur.execute("INSERT INTO expenses VALUES (NULL, ?, ?, ?, ?)", (date, amount, category, notes))
        self.conn.commit()

    def view_all(self):
        self.cur.execute("SELECT * FROM expenses")
        return self.cur.fetchall()

    def last_edit(self):
        self.cur.execute("SELECT * FROM expenses WHERE id=(SELECT max(id) FROM expenses)")
        return self.cur.fetchone()

    def total_epxenses(self):
        self.cur.execute("SELECT SUM(amount) FROM expenses")
        return self.cur.fetchone()

    def search_date(self, date):
        self.cur.execute("SELECT * FROM expenses WHERE day=?", (date,))
        return self.cur.fetchall()

    def delete(self, id):
        self.cur.execute("DELETE FROM expenses WHERE id=?", (id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()