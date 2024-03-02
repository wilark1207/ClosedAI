import sqlite3

def add_message(author, content):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (author, content) VALUES (?, ?)', (author, content))
    conn.commit()
    conn.close()

def get_messages():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages ORDER BY id ASC')
    messages = cursor.fetchall()
    conn.close()

    return [{'id': msg[0], 'author':msg[1], 'content': msg[2]} for msg in messages]