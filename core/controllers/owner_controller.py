from PyQt5.QtWidgets import QStackedWidget, QWidget, QApplication
from ui.generated_files.UI_ODashboard import Ui_OWNER_DASHBOARD
from ui.generated_files.UI_OInventory import Ui_OWNER_INVENTORY
from ui.generated_files.UI_OOrders import Ui_OWNER_ORDERS
from ui.generated_files.UI_OSales import Ui_OWNER_SALES
from ui.generated_files.UI_OStockHistory import Ui_OWNER_STOCKHISTORY
from ui.generated_files.UI_OAccount import Ui_OWNER_ACCOUNT

from core.controllers.OInv_pageController import InventoryPageController
from core.controllers.OOrders_pageController import OrdersPageController
from core.controllers.OSales_pageController import SalesPageController
from core.controllers.OAcc_pageController import AccountPageController
from core.controllers.Date_Time import DateTimeController

class OwnerController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.stack = QStackedWidget()
        self.stack.setFixedSize(1921, 1005)
        self.current_active_button = None
        
        # Initialize DateTimeController
        self.date_time_controller = DateTimeController()
        
        # Initialize all owner pages
        self._init_dashboard()
        self._init_inventory()
        self._init_orders()
        self._init_sales()
        self._init_stock_history()
        self._init_account()
        
        # Connect date/time labels
        self.date_time_controller.add_date_time_labels(
            self.dashboard_ui.dateLabel,
            self.dashboard_ui.timeLabel
        )
        self.date_time_controller.add_date_time_labels(
            self.account_ui.dateLabel,
            self.account_ui.timeLabel
        )
        
        # Connect navigation signals
        self._connect_navigation()
        
        # Force initial state
        self.stack.setCurrentIndex(0)
        QApplication.processEvents()
        self.set_active_button('dashboard')
        QApplication.processEvents()
    
    def _init_dashboard(self):
        self.dashboard_page = QWidget()
        self.dashboard_ui = Ui_OWNER_DASHBOARD()
        self.dashboard_ui.setupUi(self.dashboard_page)
        self.stack.addWidget(self.dashboard_page)
    
    def _init_inventory(self):
        self.inventory_page = QWidget()
        self.inventory_ui = Ui_OWNER_INVENTORY()
        self.inventory_ui.setupUi(self.inventory_page)
        self.stack.addWidget(self.inventory_page)
        
        # Initialize inventory controller
        self.inventory_controller = InventoryPageController(self.inventory_ui)
    
    def _init_orders(self):
        self.orders_page = QWidget()
        self.orders_ui = Ui_OWNER_ORDERS()
        self.orders_ui.setupUi(self.orders_page)
        self.stack.addWidget(self.orders_page)
        
        # Initialize orders controller
        self.orders_controller = OrdersPageController(self.orders_ui, self)
    
    def _init_sales(self):
        self.sales_page = QWidget()
        self.sales_ui = Ui_OWNER_SALES()
        self.sales_ui.setupUi(self.sales_page)
        self.stack.addWidget(self.sales_page)
        
        # Initialize sales controller
        self.sales_controller = SalesPageController(self.sales_ui, self)
    
    def _init_stock_history(self):
        self.stock_history_page = QWidget()
        self.stock_history_ui = Ui_OWNER_STOCKHISTORY()
        self.stock_history_ui.setupUi(self.stock_history_page)
        self.stack.addWidget(self.stock_history_page)
    
    def _init_account(self):
        self.account_page = QWidget()
        self.account_ui = Ui_OWNER_ACCOUNT()
        self.account_ui.setupUi(self.account_page)
        
        # Initialize account controller
        self.account_controller = AccountPageController(self.account_ui, self)
        
        self.stack.addWidget(self.account_page)
    
    def _connect_navigation(self):
        # Store all navigation buttons for easy access
        self.nav_buttons = {
            'dashboard': self.dashboard_ui.pushButton_Dashboard,
            'inventory': self.dashboard_ui.pushButton_Inventory,
            'orders': self.dashboard_ui.pushButton_Orders,
            'sales': self.dashboard_ui.pushButton_Sales,
            'stock_history': self.dashboard_ui.pushButton_Stock_History,
            'account': self.dashboard_ui.pushButton_Account
        }
        
        # Dashboard navigation
        self.dashboard_ui.pushButton_Dashboard.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.dashboard_page), 
                    self.set_active_button('dashboard')])
        self.dashboard_ui.pushButton_Inventory.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.inventory_page), 
                    self.set_active_button('inventory')])
        self.dashboard_ui.pushButton_Orders.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.orders_page), 
                    self.set_active_button('orders')])
        self.dashboard_ui.pushButton_Sales.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.sales_page), 
                    self.set_active_button('sales')])
        self.dashboard_ui.pushButton_Stock_History.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.stock_history_page), 
                    self.set_active_button('stock_history')])
        self.dashboard_ui.pushButton_Account.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.account_page), 
                    self.set_active_button('account')])
        self.dashboard_ui.pushButton_LogOut.clicked.connect(lambda: [
            self.stack.hide(),
            self.main_controller.logout()
        ])
        
        # Dashboard quick links
        self.dashboard_ui.btnViewSalesReport.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.sales_page),
                    self.set_active_button('sales')])
        
        self.dashboard_ui.btnViewMore_Inventory.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.inventory_page),
                    self.set_active_button('inventory')])
        
        # Inventory navigation
        self.inventory_ui.pushButton_Dashboard.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.dashboard_page), 
                    self.set_active_button('dashboard')])
        self.inventory_ui.pushButton_Orders.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.orders_page), 
                    self.set_active_button('orders')])
        self.inventory_ui.pushButton_Sales.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.sales_page), 
                    self.set_active_button('sales')])
        self.inventory_ui.pushButton_Stock_History.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.stock_history_page), 
                    self.set_active_button('stock_history')])
        self.inventory_ui.pushButton_Account.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.account_page), 
                    self.set_active_button('account')])
        self.inventory_ui.pushButton_LogOut.clicked.connect(lambda: [
            self.stack.hide(),
            self.main_controller.logout()
        ])
        
        # Inventory view history button
        self.inventory_ui.pushButton_ViewHistory.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.stock_history_page),
                    self.set_active_button('stock_history')])
        
        # Orders navigation
        self.orders_ui.pushButton_Dashboard.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.dashboard_page), 
                    self.set_active_button('dashboard')])
        self.orders_ui.pushButton_Inventory.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.inventory_page), 
                    self.set_active_button('inventory')])
        self.orders_ui.pushButton_Sales.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.sales_page), 
                    self.set_active_button('sales')])
        self.orders_ui.pushButton_Stock_History.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.stock_history_page), 
                    self.set_active_button('stock_history')])
        self.orders_ui.pushButton_Account.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.account_page), 
                    self.set_active_button('account')])
        self.orders_ui.pushButton_LogOut.clicked.connect(lambda: [
            self.stack.hide(),
            self.main_controller.logout()
        ])
        
        # Sales navigation
        self.sales_ui.pushButton_Dashboard.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.dashboard_page), 
                    self.set_active_button('dashboard')])
        self.sales_ui.pushButton_Inventory.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.inventory_page), 
                    self.set_active_button('inventory')])
        self.sales_ui.pushButton_Orders.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.orders_page), 
                    self.set_active_button('orders')])
        self.sales_ui.pushButton_Stock_History.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.stock_history_page), 
                    self.set_active_button('stock_history')])
        self.sales_ui.pushButton_Account.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.account_page), 
                    self.set_active_button('account')])
        self.sales_ui.pushButton_LogOut.clicked.connect(lambda: [
            self.stack.hide(),
            self.main_controller.logout()
        ])
        
        # Stock History navigation
        self.stock_history_ui.pushButton_Dashboard.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.dashboard_page), 
                    self.set_active_button('dashboard')])
        self.stock_history_ui.pushButton_Inventory.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.inventory_page), 
                    self.set_active_button('inventory')])
        self.stock_history_ui.pushButton_Orders.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.orders_page), 
                    self.set_active_button('orders')])
        self.stock_history_ui.pushButton_Sales.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.sales_page), 
                    self.set_active_button('sales')])
        self.stock_history_ui.pushButton_Account.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.account_page), 
                    self.set_active_button('account')])
        self.stock_history_ui.pushButton_LogOut.clicked.connect(lambda: [
            self.stack.hide(),
            self.main_controller.logout()
        ])
        
        # Account navigation
        self.account_ui.pushButton_Dashboard.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.dashboard_page), 
                    self.set_active_button('dashboard')])
        self.account_ui.pushButton_Inventory.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.inventory_page), 
                    self.set_active_button('inventory')])
        self.account_ui.pushButton_Orders.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.orders_page), 
                    self.set_active_button('orders')])
        self.account_ui.pushButton_Sales.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.sales_page), 
                    self.set_active_button('sales')])
        self.account_ui.pushButton_Stock_History.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.stock_history_page), 
                    self.set_active_button('stock_history')])
        self.account_ui.pushButton_LogOut.clicked.connect(lambda: [
            self.stack.hide(),
            self.main_controller.logout()
        ])
    
    def set_active_button(self, button_name):
        """Set the active button style using direct stylesheet changes"""
        # Reset all buttons first
        for button in self.nav_buttons.values():
            button.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: black;
                    border-radius: 25px;
                    padding: 9px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #c25b55;
                    color: black;
                    font-weight: 700;
                }
            """)
        
        # Set new active button
        button = self.nav_buttons.get(button_name)
        if button:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #c25b55;
                    color: black;
                    font-weight: 700;
                    border-radius: 25px;
                    padding: 9px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #c25b55;
                    color: black;
                    font-weight: 700;
                }
            """)
            self.current_active_button = button
        
        QApplication.processEvents()
    
    def show_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_page)
        self.set_active_button('dashboard')
        self.stack.show()