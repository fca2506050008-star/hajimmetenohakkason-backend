import sqlite3

sql_statements = [
	"""CREATE TABLE IF NOT EXISTS users (
		id INTEGER PRIMARY KEY,
		password text NOT NULL,
		email text NOT NULL
	);""",

	"""INSERT INTO users (password, email) 
			VALUES ("First Task", "Hello World")
			"""
]

try:
	with sqlite3.connect('users.db') as conn:
		cursor = conn.cursor()
		
	for statement in sql_statements:
		cursor.execute(statement)
		
	conn.commit()
	
	print("Table Create")
except sqlite3.OperationalError as e:
	print("Failed to create tables:", e)