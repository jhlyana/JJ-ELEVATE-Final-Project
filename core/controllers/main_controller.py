from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QMessageBox
from ui.generated_files.UI_Landing import Ui_JJ_LANDING
from ui.generated_files.UI_LogIn import Ui_LOGIN
from core.controllers.owner_controller import OwnerController
from core.controllers.cashier_controller import CashierController
from core.controllers.forgotpass_controller import ForgotPasswordController
from database import Database

class MainController:
    def __init__(self):
        self.database = Database()
        self.database.connect()
        
        # Initialize controllers without user_id first
        self.owner_controller = None
        self.cashier_controller = None
        self.current_user_id = None  # Track current user ID

        # Auth stack
        self.auth_stack = QStackedWidget()
        self.auth_stack.setFixedSize(1921, 1005)

        # Initialize pages
        self._init_landing_page()
        self._init_login_page()

        # Forgot password controller
        self.forgot_pass_controller = ForgotPasswordController()
        self.forgot_pass_controller.hide()

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
        self.login_ui.pushButton_LOGIN.clicked.connect(self.attempt_login)
        self.login_ui.pushButton_forgotPass_login_page.clicked.connect(self.show_forgot_pass)
        self.login_ui.pushButton_xtolanding.clicked.connect(self.show_landing)
        self.auth_stack.addWidget(self.login_page)

    def show_landing(self):
        self.auth_stack.setCurrentWidget(self.landing_page)
        self.auth_stack.show()

    def show_login(self):
        self.auth_stack.setCurrentWidget(self.login_page)
        self.auth_stack.show()

    def show_forgot_pass(self):
        self.forgot_pass_controller.show()
        self.auth_stack.hide()

    def attempt_login(self):
        from core.controllers.auth_controller import authenticate_user
        username = self.login_ui.login_usrname.text()
        password = self.login_ui.login_password.text()

        user = authenticate_user(username, password)

        if user is None:
            QMessageBox.warning(self.login_page, "Login Error", "Invalid username or password")
        elif user is False:
            QMessageBox.critical(self.login_page, "Login Error", "Authentication error. Please try again later.")
        else:
            # Store the user ID
            self.current_user_id = user.get("user_id")
            
            if user["role"] == "OWNER":
                if self.owner_controller is None:
                    self.owner_controller = OwnerController(self, self.database)
                self.owner_controller.show_dashboard()
            elif user["role"] == "CASHIER":
                if self.cashier_controller is None:
                    self.cashier_controller = CashierController(self, self.database, self.current_user_id)
                self.cashier_controller.show_dashboard()
            self.auth_stack.hide()

    def logout(self):
        # Hide all controller stacks
        if self.owner_controller:
            self.owner_controller.stack.hide()
        if self.cashier_controller:
            self.cashier_controller.stack.hide()

        # Clear current user
        self.current_user_id = None

        # Show auth stack and landing page
        self.auth_stack.setCurrentWidget(self.landing_page)
        self.auth_stack.show()