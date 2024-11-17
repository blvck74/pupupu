import sqlite3

# Подключаемся к базе данных и создаем таблицу, если ее нет
conn = sqlite3.connect('bot_database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS texts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section TEXT NOT NULL,
    content TEXT NOT NULL
)
''')
conn.commit()

def insert_text(section, content):
    cursor.execute('INSERT INTO texts (section, content) VALUES (?, ?)', (section, content))
    conn.commit()

def delete_text_by_id(text_id):
    cursor.execute('DELETE FROM texts WHERE id = ?', (text_id,))
    conn.commit()

def get_texts_by_section(section):
    cursor.execute('SELECT id, content FROM texts WHERE section = ?', (section,))
    return cursor.fetchall()

def delete_text_by_section_and_content(section, content):
    cursor.execute('DELETE FROM texts WHERE section = ? AND content = ?', (section, content))
    conn.commit()

# Закрываем соединение с базой данных при завершении
import atexit
@atexit.register
def close_connection():
    conn.close()
