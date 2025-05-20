class SalesPageController:
    def __init__(self, sales_ui, sales_controller):
        self.ui = sales_ui
        self.sales_controller = sales_controller
        self._setup_salestab_states()  # Initialize button states
        self._connect_sales_buttons()  # Connect button signals
        
        # Set initial page and active button
        self.ui.stackedWidget_Sales.setCurrentIndex(0)
        self.set_active_button(self.ui.pushButton_summaryView)

        # Connect the filter combo box to update the label
        self.ui.comboBox_filterSales.currentTextChanged.connect(self.update_sales_report_label)
        
        # Initialize label text based on the default combo box selection
        self.update_sales_report_label(self.ui.comboBox_filterSales.currentText())

    def _setup_salestab_states(self):
        # List of all tab buttons in the sales page
        self.sales_tab_buttons = [
            self.ui.pushButton_summaryView,
            self.ui.pushButton_salesDetail
        ]
        
        # Initialize all buttons to inactive state
        self.reset_button_styles()

    def reset_button_styles(self):
        """Reset all sales tab buttons to inactive state"""
        for button in self.sales_tab_buttons:  
            button.setProperty('class', '')
            button.style().unpolish(button)
            button.style().polish(button)

    def _connect_sales_buttons(self):
        """Connect the sales tab buttons to their respective functions"""
        self.ui.pushButton_summaryView.clicked.connect(lambda: self.view_sales_tab(0))
        self.ui.pushButton_salesDetail.clicked.connect(lambda: self.view_sales_tab(1))

    def set_active_button(self, button):
        """Set a single button as active"""
        self.reset_button_styles()  # First reset all buttons
        button.setProperty('class', 'activeButton')
        button.style().unpolish(button)
        button.style().polish(button)
        
    def view_sales_tab(self, index):
        """Switch to the specified sales tab and update button states"""
        self.ui.stackedWidget_Sales.setCurrentIndex(index)
        
        # Set the appropriate button as active based on the index
        if index == 0:
            self.set_active_button(self.ui.pushButton_summaryView)
        elif index == 1:
            self.set_active_button(self.ui.pushButton_salesDetail)

    def update_sales_report_label(self, filter_text):
        """Update the sales report label based on the selected filter"""
        filter_text = filter_text.upper()  
        
        if filter_text == "DAILY":
            self.ui.SALES_label.setText("Daily Sales Report")
        elif filter_text == "WEEKLY":
            self.ui.SALES_label.setText("Weekly Sales Report")
        elif filter_text == "MONTHLY":
            self.ui.SALES_label.setText("Monthly Sales Report")
        else:
            self.ui.SALES_label.setText("Sales Report")   # Default/fallback