import os
import psycopg2

ALLOWED_TABLES = {"accounts"}
ALLOWED_SORT_COLUMNS = {"created_at", "email", "id"}
ALLOWED_SORT_DIR = {"ASC", "DESC"}

def find_accounts_advanced(
    table_name: str,
    email: str,
    status: str = "active",
    role: str = "user",
    search: str = "",
    sort_by: str = "created_at",
    sort_dir: str = "DESC",
    limit: int = 50,
    offset: int = 0,
):
     if table_name not in ALLOWED_TABLES:
        raise ValueError("Invalid table name")
    if sort_by not in ALLOWED_SORT_COLUMNS:
        raise ValueError("Invalid sort column")
    if sort_dir not in ALLOWED_SORT_DIR:
        raise ValueError("Invalid sort direction")
    query = f"""
        SELECT id, email, created_at, role
        FROM {table_name}
        WHERE email LIKE %s
          AND status = %s
          AND role = %s
          AND (email LIKE %s OR CAST(id AS TEXT) LIKE %s)
        ORDER BY {sort_by} {sort_dir}
        LIMIT %s OFFSET %s;
    """
    params = (
        f"%{email}%",
        status,
        role,
        f"%{search}%",
        f"%{search}%",
        limit,
        offset,
    )
    conn = psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        dbname=os.getenv("PGDATABASE", "testdb"),
        user=os.getenv("PGUSER", "testuser"),
        password=os.getenv("PGPASSWORD", "testpass"),
    )
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()
    finally:
        conn.close()
