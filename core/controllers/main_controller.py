from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget
from ui.generated_files.UI_Landing import Ui_JJ_LANDING
from ui.generated_files.UI_LogIn import Ui_LOGIN
from ui.generated_files.UI_ForgotPass import Ui_ForgotPass
from core.controllers.owner_controller import OwnerController
from core.controllers.cashier_controller import CashierController

class MainController: # Create the main controller to handle navigation
    def __init__(self):
        # Initialize all controllers
        self.owner_controller = OwnerController(self)
        self.cashier_controller = CashierController(self)
        
        # Create main stacked widget for auth pages
        self.auth_stack = QStackedWidget()
        
        # Initialize auth pages
        self._init_landing_page()
        self._init_login_page()
        self._init_forgot_pass_page()
        
    def _init_landing_page(self):
        self.landing_page = QWidget()
        self.landing_ui = Ui_JJ_LANDING()
        self.landing_ui.setupUi(self.landing_page)
        
        # Connect signals
        self.landing_ui.pushButton_cont_2Login.clicked.connect(self.show_login)
        
        # Add to stack
        self.auth_stack.addWidget(self.landing_page)
    
    def _init_login_page(self):
        self.login_page = QWidget()
        self.login_ui = Ui_LOGIN()
        self.login_ui.setupUi(self.login_page)
        
        # Connect signals
        self.login_ui.pushButton_LOGIN.clicked.connect(self.attempt_login)
        self.login_ui.pushButton_forgotPass_login_page.clicked.connect(self.show_forgot_pass)
        self.login_ui.pushButton_xtolanding.clicked.connect(self.show_landing)
        
        # Add to stack
        self.auth_stack.addWidget(self.login_page)
    
    def _init_forgot_pass_page(self):
        self.forgot_pass_page = QWidget()
        self.forgot_pass_ui = Ui_ForgotPass()
        self.forgot_pass_ui.setupUi(self.forgot_pass_page)
        
        # Connect signals
        self.forgot_pass_ui.pushButton_confirmPass_reset.clicked.connect(self.reset_password)
        self.forgot_pass_ui.pushButton_xtolanding_forgotpass_2.clicked.connect(self.show_login)
        
        # Add to stack
        self.auth_stack.addWidget(self.forgot_pass_page)
    
    def show_landing(self):
        self.auth_stack.setCurrentWidget(self.landing_page)
        self.auth_stack.show()
    
    def show_login(self):
        self.auth_stack.setCurrentWidget(self.login_page)
        self.auth_stack.show()
    
    def show_forgot_pass(self):
        self.auth_stack.setCurrentWidget(self.forgot_pass_page)
        self.auth_stack.show()
    
    def attempt_login(self):
        username = self.login_ui.login_usrname.text()
        password = self.login_ui.login_password.text()
        
        # This is a simplified login logic - you should implement proper authentication
        if username == "owner" and password == "owner123":
            self.owner_controller.show_dashboard()
            self.auth_stack.hide()
        elif username == "cashier" and password == "cashier123":
            self.cashier_controller.show_dashboard()
            self.auth_stack.hide()

    
    def reset_password(self):
        # # Implement password reset logic here
        # email = self.forgot_pass_ui.LINE_EMAIL.text()
        # print(f"Password reset requested for {email}")  # Replace with actual logic
        # self.show_login()
    
    def logout(self):
        # Clear any session data
        self.show_landing()