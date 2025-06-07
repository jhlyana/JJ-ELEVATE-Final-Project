from core.models.user_model import get_user_by_username, update_user_password
import bcrypt

def authenticate_user(username, password):
    username = username.strip()
    user = get_user_by_username(username)

    if user is None:
        return None

    try:
        stored_hash = user['user_acc_password_hash']  # Access via column name
        role = user['user_acc_role']
        user_id = user['user_acc_id']

        stored_hash_cleaned = stored_hash.strip()

        if bcrypt.checkpw(password.encode(), stored_hash_cleaned.encode()):
            return {
                "username": username, 
                "role": role,
                "user_id": user_id  # Include user_id in the return
            }
        return None
    except Exception as e:
        print(f"Auth error: {e}")
        return False

def check_username_exists(username):
    return get_user_by_username(username) is not None

def forgot_password(username, new_password):
    user = get_user_by_username(username)
    if not user:
        return False

    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode('utf-8')
    return update_user_password(username, hashed)