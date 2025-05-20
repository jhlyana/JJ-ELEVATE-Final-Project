class OrdersPageController:
    def __init__(self, orders_ui, owner_controller):
        self.ui = orders_ui
        self.owner_controller = owner_controller
        self._setup_orderstab_states()  # Initialize button states
        self._connect_orders_buttons()  # Connect button signals
        
        # Set initial page and active button
        self.ui.stackedWidget_Orders.setCurrentIndex(0)
        self.set_active_button(self.ui.pushButton_order)

    def _setup_orderstab_states(self):
        # List of all tab buttons in the orders page
        self.orders_tab_buttons = [
            self.ui.pushButton_order,
            self.ui.pushButton_orderDetail
        ]
        
        # Initialize all buttons to inactive state
        self.reset_button_styles()

    def reset_button_styles(self):
        """Reset all order tab buttons to inactive state"""
        for button in self.orders_tab_buttons:
            button.setProperty('class', '')
            button.style().unpolish(button)
            button.style().polish(button)

    def _connect_orders_buttons(self):
        """Connect the order tab buttons to their respective functions"""
        self.ui.pushButton_order.clicked.connect(lambda: self.view_orders_tab(0))
        self.ui.pushButton_orderDetail.clicked.connect(lambda: self.view_orders_tab(1))

    def set_active_button(self, button):
        """Set a single button as active"""
        self.reset_button_styles()  # First reset all buttons
        button.setProperty('class', 'activeButton')
        button.style().unpolish(button)
        button.style().polish(button)
        
    def view_orders_tab(self, index):
        """Switch to the specified orders tab and update button states"""
        self.ui.stackedWidget_Orders.setCurrentIndex(index)
        
        # Set the appropriate button as active based on the index
        if index == 0:
            self.set_active_button(self.ui.pushButton_order)
        elif index == 1:
            self.set_active_button(self.ui.pushButton_orderDetail)