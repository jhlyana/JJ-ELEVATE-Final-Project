from PyQt5.QtWidgets import QWidget, QMessageBox, QLineEdit
from PyQt5.QtCore import pyqtSignal # Import pyqtSignal
from ui.generated_files.UI_ForgotPass import Ui_ForgotPass
import re
import bcrypt
from core.models.user_model import get_user_by_username, update_user_password

class ForgotPasswordController(QWidget):
    # Define a signal to notify MainController when reset is successful
    reset_successful = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ForgotPass()
        self.ui.setupUi(self)

        # Initialize state
        self.stored_hashed_answer = None
        # self.new_pass_visible = False # Not strictly needed with QLineEdit.echoMode
        # self.confirm_pass_visible = False # Not strictly needed with QLineEdit.echoMode

        # Setup UI
        self._initialize_ui()
        self.reset_controller_state() # Call to set initial state including hiding password fields

    def _initialize_ui(self):
        # Connect buttons
        self.ui.pushButton_checkUsername.clicked.connect(self.check_username)
        self.ui.pushButton_confirmPass_reset.clicked.connect(self.reset_password)
        # Instead of self.close(), we'll emit a signal and let MainController handle hiding this window
        self.ui.pushButton_xtolanding_forgotpass_2.clicked.connect(self._emit_reset_successful)
        self.ui.pushButton_cancelPass.clicked.connect(self._emit_reset_successful) # Also connect cancel to emit signal

        # Toggle password visibility buttons
        self.ui.toggleNewPass.clicked.connect(lambda: self.toggle_password_visibility(self.ui.setNewPass, self.ui.toggleNewPass))
        self.ui.toggleConfirmPass.clicked.connect(lambda: self.toggle_password_visibility(self.ui.confirmNewPass, self.ui.toggleConfirmPass))

    def reset_controller_state(self):
        """Resets the UI elements to their initial state."""
        # Clear fields
        self.ui.checkUser.clear()
        self.ui.securityAnswerField.clear()
        self.ui.setNewPass.clear()
        self.ui.confirmNewPass.clear()
        self.ui.label_secQuestion.setText("") # Reset label text

        # Disable and hide password/answer related fields
        self.ui.securityAnswerField.setEnabled(False)
        self.ui.setNewPass.setEnabled(False)
        self.ui.confirmNewPass.setEnabled(False)
        self.ui.pushButton_confirmPass_reset.setEnabled(False)

        # Hide password input fields and their labels/toggle buttons directly
        # You might need to adjust these based on your UI_ForgotPass.py structure.
        # Assuming your UI has these as separate widgets that can be hidden.
        self.ui.setNewPass.hide()
        self.ui.confirmNewPass.hide()
        self.ui.toggleNewPass.hide()
        self.ui.toggleConfirmPass.hide()
        # If you have labels for "New Password" and "Confirm New Password", hide them too
        # For example: self.ui.label_new_pass.hide() if you have such labels

        # Ensure password fields are in password mode initially
        self.ui.setNewPass.setEchoMode(QLineEdit.Password)
        self.ui.confirmNewPass.setEchoMode(QLineEdit.Password)

        # Show check username elements
        self.ui.checkUser.show() # Make sure the username input is visible
        self.ui.pushButton_checkUsername.show() # And its button

    def toggle_password_visibility(self, field, button):
        if field.echoMode() == QLineEdit.Password:
            field.setEchoMode(QLineEdit.Normal)
            button.setText("")
        else:
            field.setEchoMode(QLineEdit.Password)
            button.setText("")

    def check_username(self):
        username = self.ui.checkUser.text().strip()
        if not username:
            QMessageBox.warning(self, "Error", "Please enter a username")
            return

        user = get_user_by_username(username)

        if not user:
            QMessageBox.warning(self, "Error", "Username not found")
            return

        role = user.get('user_acc_role') # Use .get() for safer access
        security_question = user.get('security_question')
        security_answer = user.get('security_answer')

        if role != "OWNER":
            QMessageBox.warning(self, "Access Denied", "Only OWNER accounts can reset passwords")
            return

        if not security_question or not security_answer:
            QMessageBox.warning(self, "Error", "Security question not set for this account")
            return

        # Show security question and enable answer field
        self.ui.label_secQuestion.setText(security_question)
        self.ui.securityAnswerField.setEnabled(True)

        # Show and enable password fields and their toggle buttons
        self.ui.setNewPass.show()
        self.ui.confirmNewPass.show()
        self.ui.toggleNewPass.show()
        self.ui.toggleConfirmPass.show()
        self.ui.setNewPass.setEnabled(True)
        self.ui.confirmNewPass.setEnabled(True)
        self.ui.pushButton_confirmPass_reset.setEnabled(True)

        # Store the hashed answer
        self.stored_hashed_answer = security_answer.strip()

    def _emit_reset_successful(self):
        """Emits the signal and hides the current widget."""
        self.reset_successful.emit()
        self.hide() # Hide this window, MainController will show the login page

    def reset_password(self):
        # Get inputs
        answer = self.ui.securityAnswerField.text().strip()
        new_pass = self.ui.setNewPass.text()
        confirm_pass = self.ui.confirmNewPass.text()

        # Validations
        if not answer:
            QMessageBox.warning(self, "Error", "Please answer the security question")
            return

        # Ensure stored_hashed_answer is available before checking
        if not self.stored_hashed_answer:
            QMessageBox.critical(self, "Error", "Security answer not loaded. Please re-check username.")
            return

        try:
            if not bcrypt.checkpw(answer.encode('utf-8'), self.stored_hashed_answer.encode('utf-8')):
                QMessageBox.warning(self, "Error", "Incorrect security answer")
                return
        except ValueError:
            QMessageBox.critical(self, "Error", "Error processing security answer. It might be malformed.")
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
        hashed = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        username = self.ui.checkUser.text().strip()

        if update_user_password(username, hashed):
            QMessageBox.information(self, "Success", "Password updated successfully!")
            self._emit_reset_successful() # Emit signal instead of closing
        else:
            QMessageBox.critical(self, "Error", "Failed to update password")