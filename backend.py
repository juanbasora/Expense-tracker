import sqlite3

class Database:

	def __init__(self):
		self.conn = sqlite3.connect("expenses.db")
		self.cur = self.conn.cursor()
		self.cur.execute("CREATE TABLE IF NOT EXISTS expenses (date text, amount integer, category text, notes text)")
		self.conn.commit()

	def add_entry(self, date, amount, category, notes):
		self.cur.execute("INSERT INTO expenses VALUES (?, ?, ?, ?)", (date, amount, category, notes))
		self.conn.commit()

	def view_all(self):
		self.cur.execute("SELECT * FROM expenses")
		rows = self.cur.fetchall()
		return rows

	def search(self, title=""):
		self.cur.execute("SELECT * FROM expenses WHERE title=? OR author=? OR year=? OR isbn=?", (date, amount, category, notes))
		rows = self.cur.fetchall()
		return rows

	def delete(self, id):
		self.cur.execute("DELETE FROM expenses WHERE id=?", (id,))
		self.conn.commit()

	def __del__(self):
		self.conn.close()