from PyQt5.QtWidgets import QStackedWidget, QWidget
from ui.generated_files.UI_ODashboard import Ui_OWNER_DASHBOARD
from ui.generated_files.UI_OInventory import Ui_OWNER_INVENTORY
from ui.generated_files.UI_OOrders import Ui_OWNER_ORDERS
from ui.generated_files.UI_OSales import Ui_OWNER_SALES
from ui.generated_files.UI_OStockHistory import Ui_OWNER_STOCKHISTORY
from ui.generated_files.UI_OAccount import Ui_OWNER_ACCOUNT

class OwnerController: #Create the Owner interface controller
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.stack = QStackedWidget()
        
        # Initialize all owner pages
        self._init_dashboard()
        self._init_inventory()
        self._init_orders()
        self._init_sales()
        self._init_stock_history()
        self._init_account()
        
        # Connect navigation signals
        self._connect_navigation()
    
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
    
    def _init_orders(self):
        self.orders_page = QWidget()
        self.orders_ui = Ui_OWNER_ORDERS()
        self.orders_ui.setupUi(self.orders_page)
        self.stack.addWidget(self.orders_page)
    
    def _init_sales(self):
        self.sales_page = QWidget()
        self.sales_ui = Ui_OWNER_SALES()
        self.sales_ui.setupUi(self.sales_page)
        self.stack.addWidget(self.sales_page)
    
    def _init_stock_history(self):
        self.stock_history_page = QWidget()
        self.stock_history_ui = Ui_OWNER_STOCKHISTORY()
        self.stock_history_ui.setupUi(self.stock_history_page)
        self.stack.addWidget(self.stock_history_page)
    
    def _init_account(self):
        self.account_page = QWidget()
        self.account_ui = Ui_OWNER_ACCOUNT()
        self.account_ui.setupUi(self.account_page)
        self.stack.addWidget(self.account_page)
    
    def _connect_navigation(self):
        # Dashboard navigation
        self.dashboard_ui.pushButton_Inventory.clicked.connect(lambda: self.stack.setCurrentWidget(self.inventory_page))
        self.dashboard_ui.pushButton_Orders.clicked.connect(lambda: self.stack.setCurrentWidget(self.orders_page))
        self.dashboard_ui.pushButton_Sales.clicked.connect(lambda: self.stack.setCurrentWidget(self.sales_page))
        self.dashboard_ui.pushButton_Stock_History.clicked.connect(lambda: self.stack.setCurrentWidget(self.stock_history_page))
        self.dashboard_ui.pushButton_Account.clicked.connect(lambda: self.stack.setCurrentWidget(self.account_page))
        self.dashboard_ui.pushButton_LogOut.clicked.connect(self.main_controller.logout)
        
        # Inventory navigation
        self.inventory_ui.pushButton_Dashboard.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))
        self.inventory_ui.pushButton_Orders.clicked.connect(lambda: self.stack.setCurrentWidget(self.orders_page))
        self.inventory_ui.pushButton_Sales.clicked.connect(lambda: self.stack.setCurrentWidget(self.sales_page))
        self.inventory_ui.pushButton_Stock_History.clicked.connect(lambda: self.stack.setCurrentWidget(self.stock_history_page))
        self.inventory_ui.pushButton_Account.clicked.connect(lambda: self.stack.setCurrentWidget(self.account_page))
        self.inventory_ui.pushButton_LogOut.clicked.connect(self.main_controller.logout)
        
        # Orders navigation
        self.orders_ui.pushButton_Dashboard.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))
        self.orders_ui.pushButton_Inventory.clicked.connect(lambda: self.stack.setCurrentWidget(self.inventory_page))
        self.orders_ui.pushButton_Sales.clicked.connect(lambda: self.stack.setCurrentWidget(self.sales_page))
        self.orders_ui.pushButton_Stock_History.clicked.connect(lambda: self.stack.setCurrentWidget(self.stock_history_page))
        self.orders_ui.pushButton_Account.clicked.connect(lambda: self.stack.setCurrentWidget(self.account_page))
        self.orders_ui.pushButton_LogOut.clicked.connect(self.main_controller.logout)
        
        # Sales navigation
        self.sales_ui.pushButton_Dashboard.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))
        self.sales_ui.pushButton_Inventory.clicked.connect(lambda: self.stack.setCurrentWidget(self.inventory_page))
        self.sales_ui.pushButton_Orders.clicked.connect(lambda: self.stack.setCurrentWidget(self.orders_page))
        self.sales_ui.pushButton_Stock_History.clicked.connect(lambda: self.stack.setCurrentWidget(self.stock_history_page))
        self.sales_ui.pushButton_Account.clicked.connect(lambda: self.stack.setCurrentWidget(self.account_page))
        self.sales_ui.pushButton_LogOut.clicked.connect(self.main_controller.logout)
        
        # Stock History navigation
        self.stock_history_ui.pushButton_Dashboard.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))
        self.stock_history_ui.pushButton_Inventory.clicked.connect(lambda: self.stack.setCurrentWidget(self.inventory_page))
        self.stock_history_ui.pushButton_Orders.clicked.connect(lambda: self.stack.setCurrentWidget(self.orders_page))
        self.stock_history_ui.pushButton_Sales.clicked.connect(lambda: self.stack.setCurrentWidget(self.sales_page))
        self.stock_history_ui.pushButton_Account.clicked.connect(lambda: self.stack.setCurrentWidget(self.account_page))
        self.stock_history_ui.pushButton_LogOut.clicked.connect(self.main_controller.logout)
        
        # Account navigation
        self.account_ui.pushButton_Dashboard.clicked.connect(lambda: self.stack.setCurrentWidget(self.dashboard_page))
        self.account_ui.pushButton_Inventory.clicked.connect(lambda: self.stack.setCurrentWidget(self.inventory_page))
        self.account_ui.pushButton_Orders.clicked.connect(lambda: self.stack.setCurrentWidget(self.orders_page))
        self.account_ui.pushButton_Sales.clicked.connect(lambda: self.stack.setCurrentWidget(self.sales_page))
        self.account_ui.pushButton_Stock_History.clicked.connect(lambda: self.stack.setCurrentWidget(self.stock_history_page))
        self.account_ui.pushButton_LogOut.clicked.connect(self.main_controller.logout)
    
    def show_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_page)
        self.stack.show()