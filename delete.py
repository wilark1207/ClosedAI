import sqlite3

conn = sqlite3.connect('messages.db')
cursor = conn.cursor()
cursor.execute('DELETE FROM messages')
conn.commit()
conn.close()