import sqlite3
import os

TABLE = "todos_items"
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        f"CREATE TABLE IF NOT EXISTS {TABLE} ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "description TEXT NOT NULL, "
        "done INTEGER NOT NULL DEFAULT 0)"
    )
    conn.commit()
    conn.close()

def create_todo(description):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"INSERT INTO {TABLE} (description) VALUES (?)", (description,))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return new_id

def list_todos():
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT id, description, done FROM {TABLE} ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_todo(todo_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT id, description, done FROM {TABLE} WHERE id = ?", (todo_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def update_todo(todo_id, description=None, done=None):
    conn = get_connection()
    c = conn.cursor()

    fields = []
    values = []

    if description is not None:
        fields.append("description = ?")
        values.append(description)
    if done is not None:
        fields.append("done = ?")
        values.append(1 if done else 0)
    if not fields:
        conn.close()
        return False

    values.append(todo_id)
    sql = f"UPDATE {TABLE} SET {', '.join(fields)} WHERE id = ?"
    c.execute(sql, values)
    conn.commit()
    conn.close()
    return get_todo(todo_id)

def delete_todo(todo_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"DELETE FROM {TABLE} WHERE id = ?", (todo_id,))
    conn.commit()
    deleted = c.rowcount > 0
    conn.close()
    return deleted