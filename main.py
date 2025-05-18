import sys
from PyQt5.QtWidgets import QApplication
from ui.generated_files.UI_Landing import Ui_JJ_LANDING
from core.controllers.main_controller import MainController

def main():
    app = QApplication(sys.argv)
    
    # Initialize the main controller
    controller = MainController()
    
    # Show the landing page
    controller.show_landing()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()