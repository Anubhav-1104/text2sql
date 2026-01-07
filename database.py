import sqlite3

DB_PATH = "Chinook_Sqlite.sqlite"

def check_against_db(query: str):
    # basic safety: allow only SELECT
    query_lower = query.strip().lower()

    if not query_lower.startswith("select"):
        raise Exception("Only SELECT queries are allowed")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    finally:
        conn.close()

def get_schema(db_path="Chinook_Sqlite.sqlite"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name FROM sqlite_master WHERE type='table';
    """)
    tables = cursor.fetchall()

    schema = {}

    for (table,) in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        schema[table] = [col[1] for col in columns]

    conn.close()
    return schema


def format_schema(schema: dict):
    text = "Database schema:\n"

    for table, columns in schema.items():
        text += f"\nTable: {table}\nColumns: {', '.join(columns)}\n"

    return text
