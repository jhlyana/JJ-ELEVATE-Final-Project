from PyQt5.QtWidgets import QWidget, QMessageBox, QLineEdit
from ui.generated_files.UI_ForgotPass import Ui_ForgotPass
import re
import bcrypt
from core.models.user_model import get_user_by_username, update_user_password

class ForgotPasswordController(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ForgotPass()
        self.ui.setupUi(self)

        # Initialize state
        self.stored_hashed_answer = None
        self.new_pass_visible = False
        self.confirm_pass_visible = False

        # Setup UI
        self._initialize_ui()

    def _initialize_ui(self):
        # Disable password fields initially
        self.ui.setNewPass.setEnabled(False)
        self.ui.confirmNewPass.setEnabled(False)
        self.ui.pushButton_confirmPass_reset.setEnabled(False)
        self.ui.securityAnswerField.setEnabled(False)

        # Set password fields to hidden
        self.ui.setNewPass.setEchoMode(QLineEdit.Password)
        self.ui.confirmNewPass.setEchoMode(QLineEdit.Password)

        # Connect buttons
        self.ui.pushButton_checkUsername.clicked.connect(self.check_username)
        self.ui.pushButton_confirmPass_reset.clicked.connect(self.reset_password)
        self.ui.pushButton_xtolanding_forgotpass_2.clicked.connect(self.close)

        # Toggle password visibility buttons
        self.ui.toggleNewPass.clicked.connect(lambda: self.toggle_password_visibility(self.ui.setNewPass, self.ui.toggleNewPass))
        self.ui.toggleConfirmPass.clicked.connect(lambda: self.toggle_password_visibility(self.ui.confirmNewPass, self.ui.toggleConfirmPass))

    def toggle_password_visibility(self, field, button):
        if field.echoMode() == QLineEdit.Password:
            field.setEchoMode(QLineEdit.Normal)
            button.setText("Hide")
        else:
            field.setEchoMode(QLineEdit.Password)
            button.setText("Show")

    def check_username(self):
        username = self.ui.checkUser.text().strip()
        if not username:
            QMessageBox.warning(self, "Error", "Please enter a username")
            return

        user = get_user_by_username(username)

        if not user:
            QMessageBox.warning(self, "Error", "Username not found")
            return

        _, _, role, security_question, security_answer = user

        if role != "OWNER":
            QMessageBox.warning(self, "Access Denied", "Only OWNER accounts can reset passwords")
            return

        if not security_question or not security_answer:
            QMessageBox.warning(self, "Error", "Security question not set for this account")
            return

        # Show security question
        self.ui.label_secQuestion.setText(security_question)
        self.ui.securityAnswerField.setEnabled(True)
        self.ui.setNewPass.setEnabled(True)
        self.ui.confirmNewPass.setEnabled(True)
        self.ui.pushButton_confirmPass_reset.setEnabled(True)

        # *** CRITICAL FIX: Strip any whitespace from the stored answer hash ***
        self.stored_hashed_answer = security_answer.strip()

    def reset_password(self):
        # Get inputs
        answer = self.ui.securityAnswerField.text().strip()
        new_pass = self.ui.setNewPass.text()
        confirm_pass = self.ui.confirmNewPass.text()

        # Validations
        if not answer:
            QMessageBox.warning(self, "Error", "Please answer the security question")
            return

        # Use the stripped stored_hashed_answer
        if not bcrypt.checkpw(answer.encode(), self.stored_hashed_answer.encode()):
            QMessageBox.warning(self, "Error", "Incorrect security answer")
            return

        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Error", "Passwords don't match")
            return

        if len(new_pass) < 8:
            QMessageBox.warning(self, "Error", "Password must be at least 8 characters")
            return

        if not (any(c.isupper() for c in new_pass) and
                any(c in '!@#$%^&*(),.?":{}|<>' for c in new_pass)):
            QMessageBox.warning(self, "Error",
                                "Password must contain:\n- 1 uppercase letter\n- 1 special character")
            return

        # Update password
        hashed = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt()).decode('utf-8')
        username = self.ui.checkUser.text().strip()

        if update_user_password(username, hashed):
            QMessageBox.information(self, "Success", "Password updated successfully!")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Failed to update password")