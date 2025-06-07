import psycopg2
from psycopg2 import sql

def get_db_connection():
    return psycopg2.connect(
        dbname="inventory_sales_system",
        user="postgres",
        password="",
        host="localhost"
    )

def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT user_acc_id, user_acc_username, user_acc_password_hash, 
                   user_acc_role, shop_id, security_question, security_answer
            FROM user_account 
            WHERE user_acc_username = %s
        """, (username,))
        
        # Convert result to dictionary
        columns = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        if row:
            return dict(zip(columns, row))
        return None
    finally:
        cursor.close()
        conn.close()

def update_user_password(username, new_hash):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE user_account 
            SET user_acc_password_hash = %s 
            WHERE user_acc_username = %s
        """, (new_hash, username))
        
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Update error: {e}")
        return False
    finally:
        if conn:
            conn.close()
            
def authenticate_user(username, password):
    username = username.strip()
    user = get_user_by_username(username)

    if user is None:
        return None

    try:
        stored_hash = user['user_acc_password_hash']
        role = user['user_acc_role']
        user_id = user['user_acc_id']

        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            return {
                "username": username, 
                "role": role,
                "user_id": user_id
            }
        return None
    except Exception as e:
        print(f"Auth error: {e}")
        return False