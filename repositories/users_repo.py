from db import get_db_conn


CREATE_USER_QUERY = """
    INSERT INTO users (name, email, phone, role, is_active)
    VALUES (%s, %s, %s, %s, TRUE)
    RETURNING id;
"""

SELECT_USERS_BASE_QUERY = """
    SELECT id, name, email, phone, role, is_active
    FROM users
"""

TOGGLE_USER_ACTIVE_STATUS_QUERY = """
    UPDATE users
    SET is_active = NOT is_active
    WHERE id = %s
    RETURNING id, is_active;
"""

def create_user(name, email, phone, role):
    with get_db_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_USER_QUERY, (name, email, phone, role))
            row = cursor.fetchone()
            conn.commit()
            return row[0] if row else None

def toggle_user_active_status(user_id):
    with get_db_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(TOGGLE_USER_ACTIVE_STATUS_QUERY, (user_id,))
            row = cursor.fetchone()
            conn.commit()
            return row

def get_single_user_details(user_id):
    query = SELECT_USERS_BASE_QUERY + """
    WHERE id = %s;
"""

    with get_db_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id))
            row = cursor.fetchone()
            return row

def get_users_list(page_num = 1, page_size = 10, role = None):
    query = SELECT_USERS_BASE_QUERY + """
    WHERE is_active = TRUE
"""

    if role in ('CUSTOMER', 'STORE'):
        query += """
    AND role = %s
"""

    limit = int(page_size)
    offset = (int(page_num) - 1) * limit
    query += """
    LIMIT %s OFFSET %s
"""

    args = (role, limit, offset) if role in ('CUSTOMER', 'STORE') else (limit, offset)

    with get_db_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, args)
            rows = cursor.fetchall()

            if not rows:
                return []

            columns = ['id', 'name', 'email', 'phone', 'role']
            data = [dict(zip(columns, row)) for row in rows]
            return data