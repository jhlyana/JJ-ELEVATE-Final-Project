from PyQt5.QtWidgets import QMessageBox

class AccountPageController:
    def __init__(self, account_ui, owner_controller):
        self.ui = account_ui
        self.owner_controller = owner_controller
        self._setup_button_states()  # Initialize button states
        self._connect_account_buttons()
        
        # Set initial page - force to index 0 first before setting active button
        self.ui.stackedWidget_AccountBtns.setCurrentIndex(0)
        self.set_active_button(self.ui.pushButton_VIEW)

    def _setup_button_states(self):
        # Store all main account buttons
        self.main_buttons = [
            self.ui.pushButton_VIEW,
            self.ui.pushButton_VIEW_C,
            self.ui.pushButton_CREATE_C
        ]
        
        # Store all edit buttons
        self.edit_buttons = [
            self.ui.pushButton_EditAccount,
            self.ui.pushButton_EditAccount_cashier
        ]
        
        # Define parent-child relationships
        self.parent_buttons = {
            self.ui.pushButton_EditAccount: self.ui.pushButton_VIEW,
            self.ui.pushButton_EditAccount_cashier: self.ui.pushButton_VIEW_C
        }
        
        # Initialize all buttons to inactive state
        self.reset_button_styles()

    def reset_button_styles(self):
        """Reset all buttons to inactive state"""
        for button in self.main_buttons + self.edit_buttons:
            button.setProperty('class', '')
            button.style().unpolish(button)
            button.style().polish(button)

    def _connect_account_buttons(self):
        self.ui.pushButton_VIEW.clicked.connect(self.view_owner_account)
        self.ui.pushButton_EditAccount.clicked.connect(self.edit_owner_account)
        self.ui.pushButton_VIEW_C.clicked.connect(self.view_cashier_account)
        self.ui.pushButton_EditAccount_cashier.clicked.connect(self.edit_cashier_account)
        self.ui.pushButton_CREATE_C.clicked.connect(self.create_cashier_account)

    def set_active_button(self, button):
        """Set a single button as active and maintain parent button state"""
        self.reset_button_styles()  # First reset all buttons
        button.setProperty('class', 'activeButton')
        button.style().unpolish(button)
        button.style().polish(button)
        
        # Activate parent button if this is an edit button
        parent_button = self.parent_buttons.get(button)
        if parent_button:
            parent_button.setProperty('class', 'activeButton')
            parent_button.style().unpolish(parent_button)
            parent_button.style().polish(parent_button)

    def view_owner_account(self):
        self.ui.stackedWidget_AccountBtns.setCurrentIndex(0)
        self.set_active_button(self.ui.pushButton_VIEW)

    def edit_owner_account(self):
        self.ui.stackedWidget_AccountBtns.setCurrentIndex(1)
        self.set_active_button(self.ui.pushButton_EditAccount)
        self.ui.pushButton_saveEditaccount.clicked.connect(self.save_owner_edit)

    def save_owner_edit(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText("Owner account has been updated!")
        msg.exec_()
        self.view_owner_account()

    def view_cashier_account(self):
        self.ui.stackedWidget_AccountBtns.setCurrentIndex(2)
        self.set_active_button(self.ui.pushButton_VIEW_C)

    def edit_cashier_account(self):
        self.ui.stackedWidget_AccountBtns.setCurrentIndex(3)
        self.set_active_button(self.ui.pushButton_EditAccount_cashier)
        self.ui.pushButton_saveEditaccount_cashier.clicked.connect(self.save_cashier_edit)

    def save_cashier_edit(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText("Cashier account has been updated!")
        msg.exec_()
        self.view_cashier_account()

    def create_cashier_account(self):
        self.ui.stackedWidget_AccountBtns.setCurrentIndex(4)
        self.set_active_button(self.ui.pushButton_CREATE_C)
        self.ui.pushButton_CreateAccount_cashier.clicked.connect(self.handle_cashier_account_creation)
        self.ui.pushButton_cancelCreateAccount_cashier.clicked.connect(self.view_cashier_account)
        
    def handle_cashier_account_creation(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText("CASHIER account has been created!")
        msg.exec_()
        self.view_cashier_account()