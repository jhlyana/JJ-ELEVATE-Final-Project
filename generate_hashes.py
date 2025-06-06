# generate_hashes.py
import bcrypt

def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return hashed

def hash_security_answer(answer):
    hashed = bcrypt.hashpw(answer.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return hashed

print("--- Hashes for Aowner ---")
owner_password = "AaronOwner123"
owner_security_answer = "fluffy"
print(f"Owner Password Hash: '{hash_password(owner_password)}'")
print(f"Owner Security Answer Hash: '{hash_security_answer(owner_security_answer)}'")

print("\n--- Hashes for Cashier ---")
cashier_password = "OnlyCashier123"
cashier_security_answer = "spot"
print(f"Cashier Password Hash: '{hash_password(cashier_password)}'")
print(f"Cashier Security Answer Hash: '{hash_security_answer(cashier_security_answer)}'")