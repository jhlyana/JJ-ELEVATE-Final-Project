# main_controller.py
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QMessageBox, QLineEdit
from PyQt5.QtCore import QSettings # Import QSettings for remembering me
from ui.generated_files.UI_Landing import Ui_JJ_LANDING
from ui.generated_files.UI_LogIn import Ui_LOGIN
from ui.generated_files.UI_ForgotPass import Ui_ForgotPass
from core.controllers.owner_controller import OwnerController
from core.controllers.cashier_controller import CashierController
from core.controllers.forgotpass_controller import ForgotPasswordController
from database import Database

class MainController:
    def __init__(self):
        self.database = Database()
        self.database.connect()
        # Initialize QSettings for "Remember Me"
        self.settings = QSettings("JJElevate", "InventorySalesSystem") # Company, Application Name
        # Initialize controllers without user_id first
        self.owner_controller = None
        self.cashier_controller = None
        self.current_user_id = None # Track current user ID
        self.current_shop_id = None # Track current shop ID
        self.current_username = None # Track current username
        
        # Auth stack
        self.auth_stack = QStackedWidget()
        self.auth_stack.setFixedSize(1921, 1005)
        
        # Initialize pages
        self._init_landing_page()
        self._init_login_page()
        
        # Forgot password controller
        self.forgot_pass_controller = ForgotPasswordController()
        self.forgot_pass_controller.hide() # Ensure it's hidden initially
        # Connect the finished signal to a slot in MainController
        self.forgot_pass_controller.reset_successful.connect(self.show_login_from_forgot_pass)

    def _init_landing_page(self):
        self.landing_page = QWidget()
        self.landing_ui = Ui_JJ_LANDING()
        self.landing_ui.setupUi(self.landing_page)
        self.landing_ui.pushButton_cont_2Login.clicked.connect(self.show_login)
        self.auth_stack.addWidget(self.landing_page)

    def _init_login_page(self):
        self.login_page = QWidget()
        self.login_ui = Ui_LOGIN()
        self.login_ui.setupUi(self.login_page)
        # Connect new login page functionalities
        self.login_ui.pushButton_LOGIN.clicked.connect(self.attempt_login)
        self.login_ui.pushButton_forgotPass_login_page.clicked.connect(self.show_forgot_pass)
        self.login_ui.pushButton_xtolanding.clicked.connect(self.show_landing)
        
        # NEW: Connect the clear logins button
        self.login_ui.pushButton_clearLogins.clicked.connect(self.clear_login_fields)
        
        # NEW: Connect the toggle password button
        self.login_ui.togglePasswordButton.clicked.connect(self.toggle_login_password_visibility)
        # NEW: Connect remember me checkbox
        self.login_ui.checkBox_rememberme.stateChanged.connect(self.remember_me_state_changed)
        self.auth_stack.addWidget(self.login_page)
        
        # Load remembered credentials when login page is initialized
        self.load_remembered_credentials()

    def show_landing(self):
        self.auth_stack.setCurrentWidget(self.landing_page)
        self.auth_stack.show()

    def show_login(self):
        # Clear login fields when showing login page, but only if remember me is not checked
        if not self.login_ui.checkBox_rememberme.isChecked():
            self.login_ui.login_usrname.clear()
            self.login_ui.login_shop_id.clear()
        self.login_ui.login_password.clear() # Always clear password for security
        
        # Ensure password field is in password mode by default when showing login
        self.login_ui.login_password.setEchoMode(QLineEdit.Password)
        # Reset toggle button text (if it changes between eye/hidden icons)
        self.login_ui.togglePasswordButton.setText("") # Assuming it's an icon
        self.auth_stack.setCurrentWidget(self.login_page)
        self.auth_stack.show()

    def show_forgot_pass(self):
        self.forgot_pass_controller.show()
        # Ensure these connections are only made once or handled carefully if the controller instance is reused
        # Disconnect previous connections to avoid multiple connections if show_forgot_pass is called multiple times
        try:
            self.forgot_pass_controller.ui.pushButton_xtolanding_forgotpass_2.clicked.disconnect(self.show_login_from_forgot_pass)
            self.forgot_pass_controller.ui.pushButton_cancelPass.clicked.disconnect(self.show_login_from_forgot_pass)
        except TypeError: # Disconnect will raise TypeError if connection doesn't exist
            pass
        self.forgot_pass_controller.ui.pushButton_xtolanding_forgotpass_2.clicked.connect(self.show_login_from_forgot_pass)
        self.forgot_pass_controller.ui.pushButton_cancelPass.clicked.connect(self.show_login_from_forgot_pass)
        self.forgot_pass_controller.reset_controller_state() # Reset the state of the forgot password controller
        self.auth_stack.hide()

    def show_login_from_forgot_pass(self):
        # This slot is called when ForgotPasswordController emits reset_successful or cancel button is clicked
        self.forgot_pass_controller.hide()
        self.show_login() # Show the login page

    def clear_login_fields(self):
        """Clears all input fields on the login page."""
        self.login_ui.login_usrname.clear()
        self.login_ui.login_password.clear()
        if hasattr(self.login_ui, 'login_shop_id'): # Check if the widget exists
            self.login_ui.login_shop_id.clear()
        # Uncheck "Remember Me" if fields are cleared manually
        self.login_ui.checkBox_rememberme.setChecked(False)
        # Ensure password field is in password mode after clearing
        self.login_ui.login_password.setEchoMode(QLineEdit.Password)
        self.login_ui.togglePasswordButton.setText("") # Reset toggle button text

    def toggle_login_password_visibility(self):
        """Toggles the visibility of the password in the login_password field."""
        if self.login_ui.login_password.echoMode() == QLineEdit.Password:
            self.login_ui.login_password.setEchoMode(QLineEdit.Normal)
            self.login_ui.togglePasswordButton.setText("") # Or set to an "eye-open" icon
        else:
            self.login_ui.login_password.setEchoMode(QLineEdit.Password)
            self.login_ui.togglePasswordButton.setText("") # Or set to an "eye-closed" icon

    def load_remembered_credentials(self):
        """Loads saved username and shop ID if 'Remember Me' was checked."""
        remember_me = self.settings.value("remember_me", False, type=bool)
        self.login_ui.checkBox_rememberme.setChecked(remember_me)
        if remember_me:
            username = self.settings.value("username", "")
            shop_id = self.settings.value("shop_id", "")
            self.login_ui.login_usrname.setText(username)
            if hasattr(self.login_ui, 'login_shop_id'):
                self.login_ui.login_shop_id.setText(shop_id)

    def remember_me_state_changed(self, state):
        """Saves or clears credentials based on 'Remember Me' checkbox state."""
        if state: # Checked
            self.settings.setValue("remember_me", True)
            self.settings.setValue("username", self.login_ui.login_usrname.text())
            if hasattr(self.login_ui, 'login_shop_id'):
                self.settings.setValue("shop_id", self.login_ui.login_shop_id.text())
        else: # Unchecked
            self.settings.setValue("remember_me", False)
            self.settings.remove("username")
            self.settings.remove("shop_id")

    def get_username_by_id(self, user_id):
        """Helper to fetch username from database given user_id."""
        query = "SELECT user_acc_username FROM user_account WHERE user_acc_id = %s"
        try:
            result = self.database.fetch_one(query, (user_id,))
            return result['user_acc_username'] if result else "N/A"
        except Exception as e:
            print(f"Error fetching username for ID {user_id}: {e}")
            return "N/A"

    def attempt_login(self):
        from core.controllers.auth_controller import authenticate_user
        username = self.login_ui.login_usrname.text()
        password = self.login_ui.login_password.text()
        shop_id_text = self.login_ui.login_shop_id.text()
        
        if not shop_id_text:
            QMessageBox.warning(self.login_page, "Login Error", "Please enter a Shop ID.")
            return
        try:
            shop_id = int(shop_id_text)
        except ValueError:
            QMessageBox.warning(self.login_page, "Login Error", "Shop ID must be a number.")
            return

        user = authenticate_user(username, password, shop_id) # Pass database instance to auth_user
        if user is None:
            QMessageBox.warning(self.login_page, "Login Error", "Invalid username, password, or Shop ID.")
        elif user is False:
            QMessageBox.critical(self.login_page, "Login Error", "Authentication error. Please try again later.")
        else:
            # Store the user ID and shop ID
            self.current_user_id = user.get("user_id")
            self.current_shop_id = user.get("shop_id") # Store the shop_id
            self.current_username = user.get("user_acc_username") # Store the username

            # If login successful and "Remember Me" is checked, save credentials
            if self.login_ui.checkBox_rememberme.isChecked():
                self.settings.setValue("username", username)
                self.settings.setValue("shop_id", shop_id_text)
            else: # If login successful but "Remember Me" is not checked, ensure they are cleared
                self.settings.remove("username")
                self.settings.remove("shop_id")
            
            if user["role"] == "OWNER":
                if self.owner_controller is None:
                    # Pass shop_id and user_id to OwnerController
                    self.owner_controller = OwnerController(self, self.database, self.current_user_id, self.current_shop_id)
                else:
                    # If controller already exists, update its user/shop context
                    self.owner_controller.current_user_id = self.current_user_id
                    self.owner_controller.current_shop_id = self.current_shop_id
                    self.owner_controller.current_username = self.current_username
                    # Re-initialize sub-controllers within OwnerController if they depend on these
                    self.owner_controller.inventory_controller = InventoryPageController(
                        inventory_ui=self.owner_controller.inventory_ui,
                        inventory_widget=self.owner_controller.inventory_page,
                        database=self.database,
                        current_user_shop_id=self.current_shop_id,
                        current_user_id=self.current_user_id,
                        current_username=self.current_username
                    )
                    self.owner_controller.stkhistory_controller = StockHistoryPageController(
                        history_ui=self.owner_controller.stock_history_ui,
                        history_widget=self.owner_controller.stock_history_page,
                        database=self.database,
                        current_user_shop_id=self.current_shop_id,
                        current_user_id=self.current_user_id,
                        current_username=self.current_username
                    )

                self.owner_controller.show_dashboard()
            elif user["role"] == "CASHIER":
                if self.cashier_controller is None:
                    # Pass shop_id to CashierController
                    self.cashier_controller = CashierController(self, self.database, self.current_user_id, self.current_shop_id)
                else:
                    # Update cashier controller context if it exists
                    self.cashier_controller.current_user_id = self.current_user_id
                    self.cashier_controller.current_shop_id = self.current_shop_id
                    # Re-initialize any sub-controllers if needed
                self.cashier_controller.show_dashboard()
            self.auth_stack.hide()

    def logout(self):
        # Hide all controller stacks
        if self.owner_controller:
            self.owner_controller.stack.hide()
        if self.cashier_controller:
            self.cashier_controller.stack.hide()
        # Clear current user and shop
        self.current_user_id = None
        self.current_shop_id = None
        self.current_username = None
        # Show auth stack and landing page
        self.auth_stack.setCurrentWidget(self.landing_page)
        self.auth_stack.show()