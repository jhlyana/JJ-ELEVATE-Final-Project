import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from ui.generated_files.UI_Landing import Ui_JJ_LANDING 
from core.controllers.main_controller import MainController
from database import Database  # Import the Database class

def main():
    app = QApplication(sys.argv) 
    
    # Initialize the main controller
    controller = MainController()
    
    # Show the landing page
    controller.show_landing()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    

# Owner account (username: Aowner, password: Aaron123!, security answer: fluffy)
# Cashier account (username: Cashieracc, password: OnlyCashier123, security answer: spot)