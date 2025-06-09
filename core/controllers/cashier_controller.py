from PyQt5.QtWidgets import QStackedWidget, QWidget
from ui.generated_files.UI_CDashboard import Ui_CASHIER_DASHBOARD
from ui.generated_files.UI_COrders import Ui_CASHIER_ORDERS
from ui.generated_files.UI_COrder_History import Ui_CASHIER_ORDER_HISTORY
from ui.generated_files.UI_CSales import Ui_CASHIER_SALES
from ui.generated_files.UI_CAccount import Ui_CASHIER_ACCOUNT
from core.controllers.CDashboard_pageController import DashboardPageController
from core.controllers.COrders_pageController import OrdersPageController
from core.controllers.COrderHistory_pageController import OrderHistoryPageController
from core.controllers.CSales_pageController import SalesPageController
from core.controllers.Date_Time import DateTimeController

class CashierController:
    def __init__(self, main_controller, database, user_id, shop_id):
        self.main_controller = main_controller
        self.database = database
        self.user_id = user_id
        self.current_shop_id = shop_id

        self.stack = QStackedWidget()
        self.stack.setFixedSize(1921, 1005)

        self.date_time_controller = DateTimeController()

        # Initialize all pages first
        self._init_dashboard()
        self._init_orders()
        self._init_order_history()
        self._init_sales()
        self._init_account()

        # Then connect navigation
        self._connect_navigation()

        # Set date time labels after UI is initialized
        self.date_time_controller.add_date_time_labels(
            self.dashboard_ui.dateLabel,
            self.dashboard_ui.timeLabel
        )
        self.date_time_controller.add_date_time_labels(
            self.account_ui.dateLabel,
            self.account_ui.timeLabel
        )

        self.stack.setCurrentIndex(0)
        self.set_active_button('dashboard')

    def _init_dashboard(self):
        self.dashboard_page = QWidget()
        self.dashboard_ui = Ui_CASHIER_DASHBOARD()
        self.dashboard_ui.setupUi(self.dashboard_page)
        self.stack.addWidget(self.dashboard_page)

        # Initialize controller after UI is set up
        self.dashboard_controller = DashboardPageController(self.dashboard_ui, self)

    def _init_orders(self):
        self.orders_page = QWidget()
        self.orders_ui = Ui_CASHIER_ORDERS()
        self.orders_ui.setupUi(self.orders_page)
        self.stack.addWidget(self.orders_page)
        self.orders_controller = OrdersPageController(self.orders_ui, self)

    def _init_order_history(self):
        self.order_history_page = QWidget()
        self.order_history_ui = Ui_CASHIER_ORDER_HISTORY()
        self.order_history_ui.setupUi(self.order_history_page)
        self.stack.addWidget(self.order_history_page)
        self.orderHistory_controller = OrderHistoryPageController(self.order_history_ui, self)

    def _init_sales(self):
        self.sales_page = QWidget()
        self.sales_ui = Ui_CASHIER_SALES()
        self.sales_ui.setupUi(self.sales_page)
        self.stack.addWidget(self.sales_page)
        self.sales_controller = SalesPageController(self.sales_ui, self, self.database)

    def _init_account(self):
        self.account_page = QWidget()
        self.account_ui = Ui_CASHIER_ACCOUNT()
        self.account_ui.setupUi(self.account_page)
        self.stack.addWidget(self.account_page)

    def _connect_navigation(self):
        # Dashboard navigation
        self.dashboard_ui.pushButton_Dashboard.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.dashboard_page),
                     self.set_active_button('dashboard')])
        self.dashboard_ui.pushButton_Orders.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.orders_page),
                     self.set_active_button('orders')])
        self.dashboard_ui.pushButton_Order_History.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.order_history_page),
                     self.set_active_button('order_history')])
        self.dashboard_ui.pushButton_Sales.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.sales_page),
                     self.set_active_button('sales')])
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
        self.dashboard_ui.btnProcess_Order.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.orders_page),
                     self.set_active_button('orders')])

        # Orders navigation
        self.orders_ui.pushButton_Dashboard.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.dashboard_page),
                     self.set_active_button('dashboard')])
        self.orders_ui.pushButton_Order_History.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.order_history_page),
                     self.set_active_button('order_history')])
        self.orders_ui.pushButton_Sales.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.sales_page),
                     self.set_active_button('sales')])
        self.orders_ui.pushButton_Account.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.account_page),
                     self.set_active_button('account')])
        self.orders_ui.pushButton_LogOut.clicked.connect(lambda: [
            self.stack.hide(),
            self.main_controller.logout()
        ])

        # Order History navigation
        self.order_history_ui.pushButton_Dashboard.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.dashboard_page),
                     self.set_active_button('dashboard')])
        self.order_history_ui.pushButton_Orders.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.orders_page),
                     self.set_active_button('orders')])
        self.order_history_ui.pushButton_Sales.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.sales_page),
                     self.set_active_button('sales')])
        self.order_history_ui.pushButton_Account.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.account_page),
                     self.set_active_button('account')])
        self.order_history_ui.pushButton_LogOut.clicked.connect(lambda: [
            self.stack.hide(),
            self.main_controller.logout()
        ])
        # Sales navigation
        self.sales_ui.pushButton_Dashboard.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.dashboard_page),
                     self.set_active_button('dashboard')])
        self.sales_ui.pushButton_Orders.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.orders_page),
                     self.set_active_button('orders')])
        self.sales_ui.pushButton_Order_History.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.order_history_page),
                     self.set_active_button('order_history')])
        self.sales_ui.pushButton_Account.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.account_page),
                     self.set_active_button('account')])
        self.sales_ui.pushButton_LogOut.clicked.connect(lambda: [
            self.stack.hide(),
            self.main_controller.logout()
        ])
        # Account navigation
        self.account_ui.pushButton_Dashboard.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.dashboard_page),
                     self.set_active_button('dashboard')])
        self.account_ui.pushButton_Orders.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.orders_page),
                     self.set_active_button('orders')])
        self.account_ui.pushButton_Sales.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.sales_page),
                     self.set_active_button('sales')])
        self.account_ui.pushButton_Order_History.clicked.connect(
            lambda: [self.stack.setCurrentWidget(self.order_history_page),
                     self.set_active_button('order_history')])
        self.account_ui.pushButton_LogOut.clicked.connect(lambda: [
            self.stack.hide(),
            self.main_controller.logout()
        ])

    def set_active_button(self, button_name):
        all_nav_buttons = {
            'dashboard': [
                self.dashboard_ui.pushButton_Dashboard,
                self.orders_ui.pushButton_Dashboard,
                self.order_history_ui.pushButton_Dashboard,
                self.sales_ui.pushButton_Dashboard,
                self.account_ui.pushButton_Dashboard
            ],
            'orders': [
                self.dashboard_ui.pushButton_Orders,
                self.orders_ui.pushButton_Orders,
                self.order_history_ui.pushButton_Orders,
                self.sales_ui.pushButton_Orders,
                self.account_ui.pushButton_Orders
            ],
            'order_history': [
                self.dashboard_ui.pushButton_Order_History,
                self.orders_ui.pushButton_Order_History,
                self.order_history_ui.pushButton_Order_History,
                self.sales_ui.pushButton_Order_History,
                self.account_ui.pushButton_Order_History
            ],
            'sales': [
                self.dashboard_ui.pushButton_Sales,
                self.orders_ui.pushButton_Sales,
                self.order_history_ui.pushButton_Sales,
                self.sales_ui.pushButton_Sales,
                self.account_ui.pushButton_Sales
            ],
            'account': [
                self.dashboard_ui.pushButton_Account,
                self.orders_ui.pushButton_Account,
                self.sales_ui.pushButton_Account,
                self.order_history_ui.pushButton_Account,
                self.account_ui.pushButton_Account
            ]
        }

        for button_list in all_nav_buttons.values():
            for button in button_list:
                button.setProperty('class', '')
                button.style().unpolish(button)
                button.style().polish(button)

        active_buttons = all_nav_buttons.get(button_name, [])
        for button in active_buttons:
            button.setProperty('class', 'activeButton')
            button.style().unpolish(button)
            button.style().polish(button)

    def show_dashboard(self):
        self.stack.setCurrentWidget(self.dashboard_page)
        self.set_active_button('dashboard')
        self.stack.show()

    def refresh_dashboard(self):
        """Refreshes the data displayed on the dashboard."""
        if hasattr(self, 'dashboard_controller') and self.dashboard_controller is not None:
            print("DEBUG: Refreshing dashboard data...")
            self.dashboard_controller.update_dashboard_data()
            self.dashboard_controller.add_best_sellers_chart()
            print("DEBUG: Dashboard refreshed!")
        else:
            print("DEBUG: Dashboard controller not initialized, cannot refresh.")