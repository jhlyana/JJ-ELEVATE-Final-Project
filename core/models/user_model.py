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
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT user_acc_id, user_acc_password_hash, user_acc_role, 
                   security_question, security_answer 
            FROM user_account 
            WHERE user_acc_username = %s
        """, (username,))
        
        return cursor.fetchone()
    except Exception as e:
        print(f"Database error: {e}")
        return None
    finally:
        if conn:
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