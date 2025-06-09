import re
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSettings
from database import Database
from core.models.OAcc_pageModel import OwnerModel
from core.models.OAcc_pageModel import CashierModel  # 💡 Make sure this import exists

class AccountPageController:
    PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$')

    def __init__(self, account_ui, owner_data, parent=None):
        self.ui = account_ui
        self.owner_data = owner_data
        self.parent = parent

        self.database = Database()
        self.database.connect()

        self.owner_model = OwnerModel(self.database)
        self.cashier_model = CashierModel(self.database)

        self._setup_button_states()
        self._connect_account_buttons()

        self.ui.stackedWidget_AccountBtns.setCurrentIndex(0)
        self.set_active_button(self.ui.pushButton_VIEW)
        self.view_owner_account()

    def _setup_button_states(self):
        self.main_buttons = [
            self.ui.pushButton_VIEW,
            self.ui.pushButton_VIEW_C,
            self.ui.pushButton_CREATE_C
        ]
        self.edit_buttons = [
            self.ui.pushButton_EditAccount,
            self.ui.pushButton_EditAccount_cashier
        ]
        self.parent_buttons = {
            self.ui.pushButton_EditAccount: self.ui.pushButton_VIEW,
            self.ui.pushButton_EditAccount_cashier: self.ui.pushButton_VIEW_C
        }
         

        self.reset_button_styles()

    def reset_button_styles(self):
        for button in self.main_buttons + self.edit_buttons:
            button.setProperty('class', '')
            button.style().unpolish(button)
            button.style().polish(button)

    def _connect_account_buttons(self):
        self.ui.pushButton_VIEW.clicked.connect(self.view_owner_account)
        self.ui.pushButton_EditAccount.clicked.connect(self.edit_owner_account)
        self.ui.pushButton_VIEW_C.clicked.connect(self.view_cashier_account)
        self.ui.pushButton_EditAccount_cashier.clicked.connect(self.edit_cashier_account)
        self.ui.pushButton_cancelEditAccount_owner.clicked.connect(self.view_owner_account)
        self.ui.pushButton_cancelEditAccount_cashier.clicked.connect(self.view_cashier_account)
        self.ui.pushButton_CREATE_C.clicked.connect(self.create_cashier_account_disabled)
    
    def create_cashier_account_disabled(self):
        print("Method called!")  # Debug print
        self.show_message("Coming Soon", "Creating new cashier accounts will be available in a future update.", QMessageBox.Information)

    def set_active_button(self, button):
        self.reset_button_styles()
        button.setProperty('class', 'activeButton')
        button.style().unpolish(button)
        button.style().polish(button)

        parent_button = self.parent_buttons.get(button)
        if parent_button:
            parent_button.setProperty('class', 'activeButton')
            parent_button.style().unpolish(parent_button)
            parent_button.style().polish(parent_button)

    def view_owner_account(self):
        self.ui.stackedWidget_AccountBtns.setCurrentIndex(0)
        self.set_active_button(self.ui.pushButton_VIEW)

        owner_info = self.owner_model.get_owner_info()

        if owner_info:
            self.ui.ownerID.setText(str(owner_info.get('user_acc_id', '')))
            self.ui.ownerName.setText(owner_info.get('user_acc_username', ''))
            self.ui.ownerRole.setText(owner_info.get('user_acc_role', ''))
        else:
            self.ui.ownerID.setText('')
            self.ui.ownerName.setText('')
            self.ui.ownerRole.setText('')

    def edit_owner_account(self):
        self.ui.stackedWidget_AccountBtns.setCurrentIndex(1)
        self.set_active_button(self.ui.pushButton_EditAccount)

        try:
            self.ui.pushButton_saveEditaccount.clicked.disconnect()
        except TypeError:
            pass
        self.ui.pushButton_saveEditaccount.clicked.connect(self.save_owner_edit)

        owner_info = self.owner_model.get_owner_info()
        if owner_info:
            self.ui.userNameEnter.setText(owner_info.get('user_acc_username', ''))
            self.ui.newUserNameEnter.clear()
            self.ui.oldPassEnter.clear()
            self.ui.setPassEnter.clear()
            self.ui.confirmPassEnter.clear()

        self._setup_owner_password_toggles()

        self.ui.oldPassEnter.setEchoMode(self.ui.oldPassEnter.Password)
        self.ui.setPassEnter.setEchoMode(self.ui.setPassEnter.Password)
        self.ui.confirmPassEnter.setEchoMode(self.ui.confirmPassEnter.Password)

        self.ui.btn_toggle_old.setText("Show")
        self.ui.btn_toggle_new.setText("Show")
        self.ui.btn_toggle_confirm.setText("Show")

    def _setup_owner_password_toggles(self):
        self._attach_toggle(self.ui.oldPassEnter, self.ui.btn_toggle_old)
        self._attach_toggle(self.ui.setPassEnter, self.ui.btn_toggle_new)
        self._attach_toggle(self.ui.confirmPassEnter, self.ui.btn_toggle_confirm)

    def _setup_cashier_password_toggles(self):
        self._attach_toggle(self.ui.oldPassEnter_2, self.ui.btn_toggle_old_2)
        self._attach_toggle(self.ui.setPassEnter_2, self.ui.btn_toggle_new_2)
        self._attach_toggle(self.ui.confirmPassEnter_2, self.ui.btn_toggle_confirm_2)

    def _attach_toggle(self, line_edit, toggle_btn):
        def toggle():
            if line_edit.echoMode() == line_edit.Password:
                line_edit.setEchoMode(line_edit.Normal)
                toggle_btn.setText("Hide")
            else:
                line_edit.setEchoMode(line_edit.Password)
                toggle_btn.setText("Show")
        toggle_btn.clicked.connect(toggle)

    def save_owner_edit(self):
        new_username = self.ui.newUserNameEnter.text().strip()
        old_password = self.ui.oldPassEnter.text()
        new_password = self.ui.setPassEnter.text()
        confirm_password = self.ui.confirmPassEnter.text()

        owner_info = self.owner_model.get_owner_info()
        if not owner_info:
            self.show_message("Error", "Failed to retrieve owner information.", QMessageBox.Warning)
            return

        user_id = owner_info.get('user_acc_id')
        current_username = owner_info.get('user_acc_username')

        did_update = False

        if new_username:
            if new_username == current_username:
                self.show_message("No Change", "The new username is the same as the current one.", QMessageBox.Information)
                self.ui.newUserNameEnter.clear()
            else:
                if not self._is_valid_username(new_username):
                    self.show_message("Invalid Username", 
                                      "Username must be 3-20 characters, letters and numbers only, and contain at least one letter.",
                                      QMessageBox.Warning)
                    return
                if self.owner_model.update_username(user_id, new_username):
                    did_update = True
                    current_username = new_username
                else:
                    self.show_message("Error", "Username already exists or failed to update.", QMessageBox.Warning)
                    return

        if old_password or new_password or confirm_password:
            if not (old_password and new_password and confirm_password):
                self.show_message("Input Error", "Please complete all password fields.", QMessageBox.Warning)
                return

            if not self.owner_model.verify_password(current_username, old_password):
                self.show_message("Authentication Failed", "Old password is incorrect.", QMessageBox.Warning)
                return

            if new_password != confirm_password:
                self.show_message("Input Error", "Passwords do not match.", QMessageBox.Warning)
                return

            if not self.PASSWORD_REGEX.match(new_password):
                self.show_message("Weak Password",
                                  "Password must be at least 6 characters, include 1 uppercase letter and 1 special character.",
                                  QMessageBox.Warning)
                return

            if not self.owner_model.update_password(user_id, new_password):
                self.show_message("Error", "Failed to update password.", QMessageBox.Warning)
                return

            did_update = True

        if not did_update:
            self.show_message("No Change", "No changes were made.", QMessageBox.Information)
            return

        settings = QSettings("YourApp", "LoginCredentials")
        settings.remove("saved_username")
        settings.remove("saved_password")

        self.show_message("Security Update", "Saved login credentials cleared for security reasons.", QMessageBox.Information)
        self.show_message("Success", "Owner account has been updated!", QMessageBox.Information)

        self.ui.newUserNameEnter.clear()
        self.ui.oldPassEnter.clear()
        self.ui.setPassEnter.clear()
        self.ui.confirmPassEnter.clear()

        self.view_owner_account()

    def _is_valid_username(self, username):
        if not 3 <= len(username) <= 20:
            return False
        if not re.match(r'^[A-Za-z0-9]+$', username):
            return False
        if not re.search(r'[A-Za-z]', username):
            return False
        return True

    def show_message(self, title, message, icon=QMessageBox.Information):
        msg = QMessageBox(self.parent)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def view_cashier_account(self):
        self.ui.stackedWidget_AccountBtns.setCurrentIndex(2)
        self.set_active_button(self.ui.pushButton_VIEW_C)

        cashier_info = self.cashier_model.get_cashier_info()
        if cashier_info:
            self.ui.cashierID.setText(str(cashier_info.get('user_acc_id', '')))
            self.ui.cashierName_2.setText(cashier_info.get('user_acc_username', ''))
            self.ui.cashierRole.setText(cashier_info.get('user_acc_role', ''))
            self.cashier_data = cashier_info
        else:
            self.ui.cashierID.setText('')
            self.ui.cashierName_2.setText('')
            self.ui.cashierRole.setText('')
            self.show_message("Error", "Cashier account not found.", QMessageBox.Critical)

    def edit_cashier_account(self):
        self.ui.stackedWidget_AccountBtns.setCurrentIndex(3)
        self.set_active_button(self.ui.pushButton_EditAccount_cashier)

        try:
            self.ui.pushButton_saveEditaccount_cashier.clicked.disconnect()
        except TypeError:
            pass
        self.ui.pushButton_saveEditaccount_cashier.clicked.connect(self.save_cashier_edit)

        cashier_info = self.cashier_model.get_cashier_info()
        if cashier_info:
            self.ui.userNameEnter_2.setText(cashier_info.get('user_acc_username', ''))
            self.ui.newUserNameEnter_2.clear()
            self.ui.oldPassEnter_2.clear()
            self.ui.setPassEnter_2.clear()
            self.ui.confirmPassEnter_2.clear()

        self._setup_cashier_password_toggles()

        self.ui.oldPassEnter_2.setEchoMode(self.ui.oldPassEnter_2.Password)
        self.ui.setPassEnter_2.setEchoMode(self.ui.setPassEnter_2.Password)
        self.ui.confirmPassEnter_2.setEchoMode(self.ui.confirmPassEnter_2.Password)

        self.ui.btn_toggle_old_2.setText("Show")
        self.ui.btn_toggle_new_2.setText("Show")
        self.ui.btn_toggle_confirm_2.setText("Show")

    def save_cashier_edit(self):
        new_username = self.ui.newUserNameEnter_2.text().strip()
        old_password = self.ui.oldPassEnter_2.text()
        new_password = self.ui.setPassEnter_2.text()
        confirm_password = self.ui.confirmPassEnter_2.text()

        cashier_info = self.cashier_model.get_cashier_info()
        if not cashier_info:
            self.show_message("Error", "Failed to retrieve cashier information.", QMessageBox.Warning)
            return

        user_id = cashier_info.get('user_acc_id')
        current_username = cashier_info.get('user_acc_username')

        did_update = False

        if new_username:
            if new_username == current_username:
                self.show_message("No Change", "The new username is the same as the current one.", QMessageBox.Information)
                self.ui.newUserNameEnter_2.clear()
            else:
                if not self._is_valid_username(new_username):
                    self.show_message("Invalid Username", 
                                      "Username must be 3-20 characters, letters and numbers only, and contain at least one letter.",
                                      QMessageBox.Warning)
                    return
                if self.cashier_model.update_cashier_username(user_id, new_username):
                    did_update = True
                    current_username = new_username
                else:
                    self.show_message("Error", "Username already exists or failed to update.", QMessageBox.Warning)
                    return

        if old_password or new_password or confirm_password:
            if not (old_password and new_password and confirm_password):
                self.show_message("Input Error", "Please complete all password fields.", QMessageBox.Warning)
                return

            if not self.cashier_model.verify_cashier_password(current_username, old_password):
                self.show_message("Authentication Failed", "Old password is incorrect.", QMessageBox.Warning)
                return

            if new_password != confirm_password:
                self.show_message("Input Error", "Passwords do not match.", QMessageBox.Warning)
                return

            if not self.PASSWORD_REGEX.match(new_password):
                self.show_message("Weak Password",
                                  "Password must be at least 6 characters, include 1 uppercase letter and 1 special character.",
                                  QMessageBox.Warning)
                return

            if not self.cashier_model.update_cashier_password(user_id, new_password):
                self.show_message("Error", "Failed to update password.", QMessageBox.Warning)
                return

            did_update = True

        if not did_update:
            self.show_message("No Change", "No changes were made.", QMessageBox.Information)
            return

        self.show_message("Success", "Cashier account has been updated!", QMessageBox.Information)

        self.ui.newUserNameEnter_2.clear()
        self.ui.oldPassEnter_2.clear()
        self.ui.setPassEnter_2.clear()
        self.ui.confirmPassEnter_2.clear()

        self.view_cashier_account()

    def create_cashier_account(self):
        QMessageBox.information(
            self.parent or self.ui,  # parent widget for the message box
            "Feature Unavailable",
            "Creating a new cashier account is not available yet."
        )