import sqlite3

TABLE = "todos_items"

def get_connection():
    conn = sqlite3.connect("database.db")
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
    updated = c.rowcount > 0
    conn.close()
    return updated

def delete_todo(todo_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"DELETE FROM {TABLE} WHERE id = ?", (todo_id,))
    conn.commit()
    deleted = c.rowcount > 0
    conn.close()
    return deleted

if __name__ == "__main__":
    init_db()

    id1 = create_todo("Aprender SQLite")
    id2 = create_todo("Construir API Flask")
    print("Criados:", id1, id2)

    print("Lista:", list_todos())

    update_todo(id1, done=True)
    print("Após marcar done:", list_todos())

    delete_todo(id2)
    print("Após deletar:", list_todos())