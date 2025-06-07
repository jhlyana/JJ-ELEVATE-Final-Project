# import bcrypt

# class OwnerModel:
#     def __init__(self, database):
#         self.database = database
#         # Make sure the database connection is established
#         # The connect method should be called by the application's entry point,
#         # but a defensive check here doesn't hurt.
#         if not self.database.connection:
#             self.database.connect()

#     def get_owner_info(self):
#         """
#         Retrieves owner's user ID, username, and role.
#         """
#         try:
#             query = """
#                 SELECT user_acc_id, user_acc_username, user_acc_role
#                 FROM user_account
#                 WHERE user_acc_role = 'OWNER'
#                 LIMIT 1
#             """
#             # Use fetch_one which internally gets and closes the cursor
#             result_dict = self.database.fetch_one(query)

#             if result_dict:
#                 return {
#                     'user_acc_id': result_dict['user_acc_id'],
#                     'user_acc_username': result_dict['user_acc_username'],
#                     'user_acc_role': result_dict['user_acc_role']
#                 }
#             else:
#                 return None
#         except Exception as e:
#             print(f"[OWNER MODEL ERROR - get_owner_info]: {e}")
#             return None

#     def update_username(self, user_id, new_username):
#         """
#         Updates the owner's username.
#         Returns True on success, False otherwise.
#         """
#         try:
#             # For DML operations within a transaction, use connection.cursor() context manager
#             self.database.connection.autocommit = False # Start transaction

#             with self.database.connection.cursor() as cursor:
#                 # Check if new username already exists for another user
#                 check_query = "SELECT COUNT(*) FROM user_account WHERE user_acc_username = %s AND user_acc_id != %s"
#                 cursor.execute(check_query, (new_username, user_id))
#                 count = cursor.fetchone()[0]

#                 if count > 0:
#                     self.database.connection.rollback() # Rollback if username exists
#                     return False # Username already exists

#                 # Proceed to update
#                 update_query = "UPDATE user_account SET user_acc_username = %s WHERE user_acc_id = %s"
#                 cursor.execute(update_query, (new_username, user_id))
            
#             self.database.connection.commit() # Commit transaction
#             return True
#         except Exception as e:
#             self.database.connection.rollback() # Rollback on error
#             print(f"[OWNER MODEL ERROR - update_username]: {e}")
#             return False
#         finally:
#             self.database.connection.autocommit = True # Reset autocommit

#     def verify_password(self, username, input_password):
#         """
#         Verifies an owner's password.
#         Returns True if password is correct, False otherwise.
#         """
#         try:
#             query = "SELECT user_acc_password_hash FROM user_account WHERE user_acc_username = %s"
#             # Use fetch_one
#             result_dict = self.database.fetch_one(query, (username,))

#             if result_dict and result_dict.get('user_acc_password_hash'):
#                 stored_hashed_password = result_dict['user_acc_password_hash'].encode('utf-8')
#                 return bcrypt.checkpw(input_password.encode('utf-8'), stored_hashed_password)
#             return False
#         except Exception as e:
#             print(f"[OWNER MODEL ERROR - verify_password]: {e}")
#             return False

#     def update_password(self, user_id, new_password):
#         """
#         Updates an owner's password.
#         Returns True on success, False otherwise.
#         """
#         try:
#             self.database.connection.autocommit = False # Start transaction

#             with self.database.connection.cursor() as cursor:
#                 hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#                 query = "UPDATE user_account SET user_acc_password_hash = %s WHERE user_acc_id = %s"
#                 cursor.execute(query, (hashed_pw, user_id))
            
#             self.database.connection.commit() # Commit transaction
#             return True
#         except Exception as e:
#             self.database.connection.rollback() # Rollback on error
#             print(f"[OWNER MODEL ERROR - update_password]: {e}")
#             return False
#         finally:
#             self.database.connection.autocommit = True # Reset autocommit

#     # Add a method to get security question for password reset
#     def get_security_question(self, username):
#         try:
#             query = "SELECT security_question FROM user_account WHERE user_acc_username = %s AND user_acc_role = 'OWNER'"
#             result = self.database.fetch_one(query, (username,))
#             if result:
#                 return result.get('security_question')
#             return None
#         except Exception as e:
#             print(f"[OWNER MODEL ERROR - get_security_question]: {e}")
#             return None

#     # Add a method to verify security answer for password reset
#     def verify_security_answer(self, username, answer):
#         try:
#             query = "SELECT security_answer_hash FROM user_account WHERE user_acc_username = %s AND user_acc_role = 'OWNER'"
#             result = self.database.fetch_one(query, (username,))
#             if result and result.get('security_answer_hash'):
#                 stored_hash = result['security_answer_hash'].encode('utf-8')
#                 return bcrypt.checkpw(answer.encode('utf-8'), stored_hash)
#             return False
#         except Exception as e:
#             print(f"[OWNER MODEL ERROR - verify_security_answer]: {e}")
#             return False

#     # Add a method to get user_id by username for password reset flow
#     def get_user_id_by_username(self, username):
#         try:
#             query = "SELECT user_acc_id FROM user_account WHERE user_acc_username = %s"
#             result = self.database.fetch_one(query, (username,))
#             if result:
#                 return result.get('user_acc_id')
#             return None
#         except Exception as e:
#             print(f"[OWNER MODEL ERROR - get_user_id_by_username]: {e}")
#             return None

# import bcrypt

# class CashierModel:
#     def __init__(self, database):
#         self.database = database
#         if not self.database.connection:
#             self.database.connect()

#     def get_cashier_info(self, user_id=None): # Added optional user_id for flexibility
#         """
#         Retrieves cashier's user ID, username, and role.
#         Can retrieve specific cashier if user_id is provided, otherwise first cashier.
#         """
#         try:
#             if user_id:
#                 query = """
#                     SELECT user_acc_id, user_acc_username, user_acc_role
#                     FROM user_account
#                     WHERE user_acc_role = 'CASHIER' AND user_acc_id = %s
#                 """
#                 params = (user_id,)
#             else:
#                 query = """
#                     SELECT user_acc_id, user_acc_username, user_acc_role
#                     FROM user_account
#                     WHERE user_acc_role = 'CASHIER'
#                     LIMIT 1
#                 """
#                 params = None
            
#             # Use fetch_one which internally gets and closes the cursor
#             result_dict = self.database.fetch_one(query, params)

#             if result_dict:
#                 return {
#                     'user_acc_id': result_dict['user_acc_id'],
#                     'user_acc_username': result_dict['user_acc_username'],
#                     'user_acc_role': result_dict['user_acc_role']
#                 }
#             else:
#                 return None
#         except Exception as e:
#             print(f"[CASHIER MODEL ERROR - get_cashier_info]: {e}")
#             return None

#     def get_all_cashiers(self):
#         """
#         Retrieves a list of all cashier accounts.
#         Returns a list of dictionaries.
#         """
#         try:
#             query = """
#                 SELECT user_acc_id, user_acc_username, user_acc_role
#                 FROM user_account
#                 WHERE user_acc_role = 'CASHIER'
#                 ORDER BY user_acc_username;
#             """
#             return self.database.fetch_all(query) # Returns list of dicts
#         except Exception as e:
#             print(f"[CASHIER MODEL ERROR - get_all_cashiers]: {e}")
#             return []

#     def create_cashier_account(self, shop_id, user_role, username, password, control_password):
#         """
#         Creates a new cashier account.
#         Note: The 'control_password' handling logic might need to be verified (is it hashed/stored?).
#         For simplicity, I'm just hashing the main password.
#         """
#         try:
#             # Ensure proper transaction management
#             self.database.connection.autocommit = False 

#             with self.database.connection.cursor() as cursor:
#                 # First, check if username already exists
#                 check_username_query = "SELECT COUNT(*) FROM user_account WHERE user_acc_username = %s"
#                 cursor.execute(check_username_query, (username,))
#                 if cursor.fetchone()[0] > 0:
#                     self.database.connection.rollback()
#                     return False, "Username already exists." # Return specific error message

#                 hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#                 # Assuming 'shop_id' is directly stored or handled elsewhere
#                 # Assuming 'control_password' is not stored in user_account or needs separate hashing
                
#                 insert_query = """
#                     INSERT INTO user_account 
#                     (user_acc_username, user_acc_password_hash, user_acc_role, shop_id)
#                     VALUES (%s, %s, %s, %s) RETURNING user_acc_id;
#                 """
#                 cursor.execute(insert_query, (username, hashed_password, user_role, shop_id))
#                 new_user_id = cursor.fetchone()[0] # Get the ID of the newly created user

#             self.database.connection.commit()
#             return True, new_user_id
#         except Exception as e:
#             self.database.connection.rollback()
#             print(f"[CASHIER MODEL ERROR - create_cashier_account]: {e}")
#             return False, str(e) # Return error message
#         finally:
#             self.database.connection.autocommit = True

#     def update_cashier_username(self, user_id, new_username):
#         """
#         Updates a cashier's username.
#         Returns True on success, False otherwise.
#         """
#         try:
#             self.database.connection.autocommit = False # Start transaction

#             with self.database.connection.cursor() as cursor:
#                 # Check if the new username exists for another account
#                 check_query = "SELECT COUNT(*) FROM user_account WHERE user_acc_username = %s AND user_acc_id != %s"
#                 cursor.execute(check_query, (new_username, user_id))
#                 count = cursor.fetchone()[0]

#                 if count > 0:
#                     self.database.connection.rollback() # Rollback if username exists
#                     return False

#                 update_query = "UPDATE user_account SET user_acc_username = %s WHERE user_acc_id = %s"
#                 cursor.execute(update_query, (new_username, user_id))
            
#             self.database.connection.commit() # Commit transaction
#             return True
#         except Exception as e:
#             self.database.connection.rollback() # Rollback on error
#             print(f"[CASHIER MODEL ERROR - update_cashier_username]: {e}")
#             return False
#         finally:
#             self.database.connection.autocommit = True # Reset autocommit

#     def verify_cashier_password(self, username, input_password):
#         """
#         Verifies a cashier's password.
#         Returns True if password is correct, False otherwise.
#         """
#         try:
#             query = "SELECT user_acc_password_hash FROM user_account WHERE user_acc_username = %s"
#             result_dict = self.database.fetch_one(query, (username,))

#             if result_dict and result_dict.get('user_acc_password_hash'):
#                 stored_hash = result_dict['user_acc_password_hash'].encode('utf-8')
#                 return bcrypt.checkpw(input_password.encode('utf-8'), stored_hash)
#             return False
#         except Exception as e:
#             print(f"[CASHIER MODEL ERROR - verify_cashier_password]: {e}")
#             return False

#     def update_cashier_password(self, user_id, new_password):
#         """
#         Updates a cashier's password.
#         Returns True on success, False otherwise.
#         """
#         try:
#             self.database.connection.autocommit = False # Start transaction

#             with self.database.connection.cursor() as cursor:
#                 hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#                 query = "UPDATE user_account SET user_acc_password_hash = %s WHERE user_acc_id = %s"
#                 cursor.execute(query, (hashed_pw, user_id))
            
#             self.database.connection.commit() # Commit transaction
#             return True
#         except Exception as e:
#             self.database.connection.rollback() # Rollback on error
#             print(f"[CASHIER MODEL ERROR - update_cashier_password]: {e}")
#             return False
#         finally:
#             self.database.connection.autocommit = True # Reset autocommit

#     def delete_cashier_account(self, user_id):
#         """Deletes a cashier account by user_id."""
#         try:
#             self.database.connection.autocommit = False # Start the transaction

#             with self.database.connection.cursor() as cursor:
#                 query = "DELETE FROM user_account WHERE user_acc_id = %s AND user_acc_role = 'CASHIER';"
#                 cursor.execute(query, (user_id,))
            
#             self.database.connection.commit() # Commit the transaction
#             return True
#         except Exception as e:
#             self.database.connection.rollback() # Rollback on any error
#             print(f"Error deleting cashier account with ID {user_id}: {e}")
#             return False
#         finally:
#             self.database.connection.autocommit = True # Always reset autocommit to True