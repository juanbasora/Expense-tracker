import sqlite3

class Database:

	def __init__(self):
		self.conn = sqlite3.connect("expenses.db")
		self.cur = self.conn.cursor()
		self.cur.execute("CREATE TABLE IF NOT EXISTS expenses (day date, amount integer, category text, notes text)")
		self.conn.commit()

	def add_entry(self, day, amount, category, notes):
		self.cur.execute("INSERT INTO expenses VALUES (?, ?, ?, ?)", (day, amount, category, notes))
		self.conn.commit()

	def view_all(self):
		self.cur.execute("SELECT * FROM expenses")
		rows = self.cur.fetchall()
		return rows

	def search(self, day="", amount="", category="", notes=""):
		self.cur.execute("SELECT * FROM expenses WHERE day=? OR amount=? OR category=? OR notes=?", (day, amount, category, notes))
		rows = self.cur.fetchall()
		return rows

	def delete(self, id):
		pass

	def __del__(self):
		self.conn.close()