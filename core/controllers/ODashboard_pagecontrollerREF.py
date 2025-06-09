# from PyQt5 import QtCore, QtWidgets, QtGui
# from PyQt5.QtWidgets import QMessageBox, QLabel
# from PyQt5.QtCore import Qt
# from database import Database
# from core.models.ODashboard_pageModel import DashboardModel
# import logging

# class DashboardPageController:
#     def __init__(self, dashboard_ui, current_user_shop_id=None, current_user_id=None,
#                  current_username=None, parent=None, database_connection=None):
#         self.logger = logging.getLogger(__name__)
#         self.logger.setLevel(logging.DEBUG)
#         self.ui = dashboard_ui
#         self.current_user_shop_id = current_user_shop_id
#         self.current_user_id = current_user_id
#         self.current_username = current_username
#         self.parent = parent
        
#         if database_connection:
#             self.db = database_connection
#             self.logger.debug("Using provided database connection")
#         elif self.parent and hasattr(self.parent, 'db'):
#             self.db = self.parent.db
#             self.logger.debug("Using parent's database connection")
#         else:
#             self.db = Database()
#             try:
#                 self.db.connect()
#                 self.logger.debug("Created new database connection")
#             except Exception as e:
#                 self.logger.error(f"Failed to connect to database: {e}")
#                 QMessageBox.critical(None, "Database Error",
#                                    "Failed to initialize database connection")
#                 raise
        
#         self.dashboard_model = DashboardModel(self.db)
#         self._verify_ui_elements()
#         self._initialize_ui_state()
#         self.load_dashboard_widgets()

#     def _verify_ui_elements(self):
#         """Verify that required UI elements exist"""
#         self.lowstock_product_labels = [
#             getattr(self.ui, f'lowstock_product_label_{i}', None)
#             for i in range(1, 5)
#         ]
#         self.lowstock_qty_labels = [
#             getattr(self.ui, f'lowstock_qty_label_{i}', None)
#             for i in range(1, 5)
#         ]
#         self.logger.debug("Verifying UI elements:")
#         for i, (prod_label, qty_label) in enumerate(zip(self.lowstock_product_labels,
#                                                          self.lowstock_qty_labels), 1):
#             self.logger.debug(f"Label pair {i}: Product={prod_label is not None}, Qty={qty_label is not None}")

#     def _initialize_ui_state(self):
#         """Initialize the UI state with default values"""
#         if hasattr(self.ui, 'label_13'):
#             self.ui.label_13.setText("All items are well stocked.")
#             self.ui.label_13.setStyleSheet(
#                 "color: white; border-radius: 15px; padding: 3px; background-color: #5cb85c;"
#             )
#             self.ui.label_13.setAlignment(Qt.AlignCenter)
        
#         self._clear_low_stock_labels()
        
#         if hasattr(self.ui, 'dashb_lowinstock_value'):
#             self.ui.dashb_lowinstock_value.setText("0 items")

#     def _clear_low_stock_labels(self):
#         """Clear all low stock labels"""
#         self.logger.debug("Clearing low stock labels")
#         for label in self.lowstock_product_labels + self.lowstock_qty_labels:
#             if label:
#                 label.setText("")
#                 label.setStyleSheet("")

#     def load_dashboard_widgets(self):
#         """Load all dashboard widgets with data"""
#         self.logger.debug("Loading dashboard widgets")
#         self.load_low_stock_warning()

#     def load_low_stock_warning(self):
#         """Load and display low stock warning data"""
#         try:
#             if not self.current_user_shop_id:
#                 self.logger.error("No shop_id available")
#                 return
            
#             self.logger.debug(f"Loading low stock for shop {self.current_user_shop_id}")
            
#             total_low_stock = self.dashboard_model.get_low_stock_count(
#                 shop_id=self.current_user_shop_id
#             )
#             self.logger.debug(f"Total low stock items: {total_low_stock}")
            
#             critical_items = self.dashboard_model.get_low_stock_products(
#                 shop_id=self.current_user_shop_id,
#                 limit=4
#             )
#             self.logger.debug(f"Displaying {len(critical_items)} critical items")
            
#             if hasattr(self.ui, 'dashb_lowinstock_value'):
#                 self.ui.dashb_lowinstock_value.setText(f"{total_low_stock} items")
#                 self.logger.debug(f"Updated counter to show {total_low_stock} items")
            
#             self._clear_low_stock_labels()
            
#             if critical_items:
#                 self._display_low_stock_items(critical_items)
#             else:
#                 self._display_no_low_stock()
                
#         except Exception as e:
#             self.logger.error(f"Error loading low stock warning: {e}")
#             QMessageBox.warning(
#                 self.ui, "Low Stock Warning Error",
#                 f"Failed to load low stock data: {e}")

#     def _display_low_stock_items(self, low_stock_products):
#         """Display low stock items in the dashboard"""
#         self.logger.debug("Displaying low stock items")
        
#         if hasattr(self.ui, 'label_13'):
#             self.ui.label_13.setText("Warning! These items are low of stock.")
#             self.ui.label_13.setStyleSheet(
#                 "color: white; border-radius: 15px; padding: 3px; background-color: #c25b55;"
#             )
        
#         for i in range(4):
#             if i < len(self.lowstock_product_labels) and self.lowstock_product_labels[i]:
#                 self.lowstock_product_labels[i].setVisible(True)
#             if i < len(self.lowstock_qty_labels) and self.lowstock_qty_labels[i]:
#                 self.lowstock_qty_labels[i].setVisible(True)
        
#         for i, item_dict in enumerate(low_stock_products[:4]):
#             if i >= 4:
#                 break
            
#             product_name = item_dict.get('product_name', 'N/A')
#             current_qty = item_dict.get('prod_spec_stock_qty', 0)
            
#             if i < len(self.lowstock_product_labels) and self.lowstock_product_labels[i]:
#                 self.lowstock_product_labels[i].setText(product_name)
#                 self.lowstock_product_labels[i].setStyleSheet(
#                     "font-weight: bold; color: white; padding: 2px;"
#                 )
            
#             if i < len(self.lowstock_qty_labels) and self.lowstock_qty_labels[i]:
#                 self.lowstock_qty_labels[i].setText(f"{current_qty} left")
#                 self.lowstock_qty_labels[i].setStyleSheet(
#                     "font-weight: bold; color: #ff4757; padding: 2px;"
#                 )

#     def _display_no_low_stock(self):
#         """Display when there are no low stock items"""
#         self.logger.debug("No low stock items to display")
        
#         if hasattr(self.ui, 'label_13'):
#             self.ui.label_13.setText("All items are well stocked.")
#             self.ui.label_13.setStyleSheet(
#                 "color: white; border-radius: 15px; padding: 3px; background-color: #5cb85c;"
#             )
        
#         for i in range(4):
#             if i < len(self.lowstock_product_labels) and self.lowstock_product_labels[i]:
#                 self.lowstock_product_labels[i].setVisible(False)
#             if i < len(self.lowstock_qty_labels) and self.lowstock_qty_labels[i]:
#                 self.lowstock_qty_labels[i].setVisible(False)

#     def update_low_stock_warning(self):
#         """Update the low stock warning display"""
#         self.load_low_stock_warning()

#     def _setup_dashboard(self):
#         """Initialize dashboard components and layout"""
#         try:
#             # Setup dashboard-specific UI components
#             self._setup_dashboard_widgets()
#             self._setup_dashboard_charts()
#             self._setup_dashboard_summary_cards()
#         except Exception as e:
#             self._show_error_message(f"Error setting up dashboard: {e}")

#     def _setup_dashboard_widgets(self):
#         """Setup dashboard widgets and their properties"""
#         # Configure dashboard-specific widgets
#         pass

#     def _setup_dashboard_charts(self):
#         """Setup charts for dashboard visualization"""
#         try:
#             # Initialize charts for inventory overview
#             self._setup_inventory_overview_chart()
#             self._setup_sales_trend_chart()
#             self._setup_product_category_chart()
#         except Exception as e:
#             print(f"Error setting up dashboard charts: {e}")

#     def _setup_inventory_overview_chart(self):
#         """Setup inventory overview chart"""
#         # Implementation for inventory overview visualization
#         pass

#     def _setup_sales_trend_chart(self):
#         """Setup sales trend chart"""
#         # Implementation for sales trend visualization
#         pass

#     def _setup_product_category_chart(self):
#         """Setup product category distribution chart"""
#         # Implementation for product category visualization
#         pass

#     def _setup_dashboard_summary_cards(self):
#         """Setup summary cards for key metrics"""
#         try:
#             # Setup cards for total products, low stock items, recent additions, etc.
#             self._setup_total_products_card()
#             self._setup_low_stock_card()
#             self._setup_recent_additions_card()
#             self._setup_top_categories_card()
#         except Exception as e:
#             print(f"Error setting up summary cards: {e}")

#     def _setup_total_products_card(self):
#         """Setup total products summary card"""
#         pass

#     def _setup_low_stock_card(self):
#         """Setup low stock warning card"""
#         pass

#     def _setup_recent_additions_card(self):
#         """Setup recent additions card"""
#         pass

#     def _setup_top_categories_card(self):
#         """Setup top categories card"""
#         pass

#     def connect_dashboard_buttons(self):
#         """Connect dashboard-related buttons to their handlers"""
#         try:
#             # Connect refresh button
#             if hasattr(self.ui, 'pushButton_Dashboard_Refresh'):
#                 self.ui.pushButton_Dashboard_Refresh.clicked.connect(self.refresh_dashboard)
            
#             # Connect export button
#             if hasattr(self.ui, 'pushButton_Dashboard_Export'):
#                 self.ui.pushButton_Dashboard_Export.clicked.connect(self.export_dashboard_data)
            
#             # Connect filter buttons
#             if hasattr(self.ui, 'pushButton_Dashboard_Filter_Today'):
#                 self.ui.pushButton_Dashboard_Filter_Today.clicked.connect(lambda: self.filter_dashboard_data('today'))
            
#             if hasattr(self.ui, 'pushButton_Dashboard_Filter_Week'):
#                 self.ui.pushButton_Dashboard_Filter_Week.clicked.connect(lambda: self.filter_dashboard_data('week'))
            
#             if hasattr(self.ui, 'pushButton_Dashboard_Filter_Month'):
#                 self.ui.pushButton_Dashboard_Filter_Month.clicked.connect(lambda: self.filter_dashboard_data('month'))
                
#         except Exception as e:
#             self._show_error_message(f"Error connecting dashboard buttons: {e}")

#     def load_dashboard_data(self):
#         """Load all dashboard data and update displays"""
#         try:
#             self.update_summary_metrics()
#             self.update_inventory_overview()
#             self.update_low_stock_warnings()
#             self.update_recent_activities()
#             self.update_dashboard_charts()
#         except Exception as e:
#             self._show_error_message(f"Error loading dashboard data: {e}")

#     def update_summary_metrics(self):
#         """Update dashboard summary metrics"""
#         try:
#             # Get summary data from dashboard model
#             total_products = self.dashboard_model.get_total_products_count(self.current_user_shop_id)
#             low_stock_count = self.dashboard_model.get_low_stock_count(self.current_user_shop_id)
#             total_value = self.dashboard_model.get_total_inventory_value(self.current_user_shop_id)
            
#             # Update UI labels with summary data
#             if hasattr(self.ui, 'label_Dashboard_TotalProducts'):
#                 self.ui.label_Dashboard_TotalProducts.setText(str(total_products))
            
#             if hasattr(self.ui, 'label_Dashboard_LowStock'):
#                 self.ui.label_Dashboard_LowStock.setText(str(low_stock_count))
            
#             if hasattr(self.ui, 'label_Dashboard_TotalValue'):
#                 self.ui.label_Dashboard_TotalValue.setText(f"₱{total_value:,.2f}")
                
#         except Exception as e:
#             print(f"Error updating summary metrics: {e}")

#     def update_inventory_overview(self):
#         """Update inventory overview section"""
#         try:
#             # Get inventory overview data
#             category_data = self.dashboard_model.get_inventory_by_category(self.current_user_shop_id)
            
#             # Update category breakdown
#             for category, count in category_data.items():
#                 label_name = f'label_Dashboard_{category}_Count'
#                 if hasattr(self.ui, label_name):
#                     getattr(self.ui, label_name).setText(str(count))
                    
#         except Exception as e:
#             print(f"Error updating inventory overview: {e}")

#     def update_low_stock_warnings(self):
#         """Update low stock warning display"""
#         try:
#             low_stock_items = self.dashboard_model.get_low_stock_products(self.current_user_shop_id)
            
#             # Update low stock warning text or table
#             if hasattr(self.ui, 'textBrowser_Dashboard_LowStock'):
#                 if low_stock_items:
#                     warning_text = "LOW STOCK ALERTS:\n\n"
#                     for item in low_stock_items:
#                         warning_text += f"• {item['product_name']} - Only {item['stock_qty']} left\n"
#                     self.ui.textBrowser_Dashboard_LowStock.setText(warning_text)
#                 else:
#                     self.ui.textBrowser_Dashboard_LowStock.setText("All products are well-stocked!")
                    
#         except Exception as e:
#             print(f"Error updating low stock warnings: {e}")

#     def update_recent_activities(self):
#         """Update recent activities section"""
#         try:
#             recent_additions = self.dashboard_model.get_recent_products(self.current_user_shop_id, limit=5)
            
#             # Update recent activities display
#             if hasattr(self.ui, 'textBrowser_Dashboard_RecentActivities'):
#                 if recent_additions:
#                     activity_text = "RECENT ADDITIONS:\n\n"
#                     for product in recent_additions:
#                         activity_text += f"• {product['product_name']} - {product['created_at']}\n"
#                     self.ui.textBrowser_Dashboard_RecentActivities.setText(activity_text)
#                 else:
#                     self.ui.textBrowser_Dashboard_RecentActivities.setText("No recent activities.")
                    
#         except Exception as e:
#             print(f"Error updating recent activities: {e}")

#     def update_dashboard_charts(self):
#         """Update all dashboard charts with current data"""
#         try:
#             self._update_inventory_distribution_chart()
#             self._update_stock_level_chart()
#             self._update_value_distribution_chart()
#         except Exception as e:
#             print(f"Error updating dashboard charts: {e}")

#     def _update_inventory_distribution_chart(self):
#         """Update inventory distribution chart"""
#         try:
#             # Get distribution data
#             distribution_data = self.dashboard_model.get_inventory_distribution(self.current_user_shop_id)
            
#             # Update chart widget (implementation depends on chart library used)
#             # This would typically involve updating a QChart or similar widget
#             pass
#         except Exception as e:
#             print(f"Error updating inventory distribution chart: {e}")

#     def _update_stock_level_chart(self):
#         """Update stock level trends chart"""
#         try:
#             # Get stock level data over time
#             stock_data = self.dashboard_model.get_stock_level_trends(self.current_user_shop_id)
            
#             # Update chart widget
#             pass
#         except Exception as e:
#             print(f"Error updating stock level chart: {e}")

#     def _update_value_distribution_chart(self):
#         """Update inventory value distribution chart"""
#         try:
#             # Get value distribution data
#             value_data = self.dashboard_model.get_value_distribution(self.current_user_shop_id)
            
#             # Update chart widget
#             pass
#         except Exception as e:
#             print(f"Error updating value distribution chart: {e}")

#     def refresh_dashboard(self):
#         """Refresh all dashboard data"""
#         try:
#             self.load_dashboard_data()
#             self._show_success_message("Dashboard refreshed successfully!")
#         except Exception as e:
#             self._show_error_message(f"Error refreshing dashboard: {e}")

#     def export_dashboard_data(self):
#         """Export dashboard data to file"""
#         try:
#             # Get export data
#             export_data = self.dashboard_model.get_dashboard_export_data(self.current_user_shop_id)
            
#             # Export to CSV or Excel (implementation depends on requirements)
#             # This could involve using pandas or csv module
            
#             self._show_success_message("Dashboard data exported successfully!")
#         except Exception as e:
#             self._show_error_message(f"Error exporting dashboard data: {e}")

#     def filter_dashboard_data(self, time_period):
#         """Filter dashboard data by time period"""
#         try:
#             # Apply time filter to dashboard data
#             if time_period == 'today':
#                 filtered_data = self.dashboard_model.get_dashboard_data_today(self.current_user_shop_id)
#             elif time_period == 'week':
#                 filtered_data = self.dashboard_model.get_dashboard_data_week(self.current_user_shop_id)
#             elif time_period == 'month':
#                 filtered_data = self.dashboard_model.get_dashboard_data_month(self.current_user_shop_id)
#             else:
#                 filtered_data = None
            
#             if filtered_data:
#                 self._update_dashboard_with_filtered_data(filtered_data)
#                 self._show_success_message(f"Dashboard filtered for {time_period}")
            
#         except Exception as e:
#             self._show_error_message(f"Error filtering dashboard data: {e}")

#     def _update_dashboard_with_filtered_data(self, filtered_data):
#         """Update dashboard displays with filtered data"""
#         try:
#             # Update all dashboard components with filtered data
#             # This method would update charts, metrics, and other displays
#             # based on the filtered dataset
#             pass
#         except Exception as e:
#             print(f"Error updating dashboard with filtered data: {e}")

#     def get_dashboard_summary(self):
#         """Get dashboard summary for other controllers"""
#         try:
#             return {
#                 'total_products': self.dashboard_model.get_total_products_count(self.current_user_shop_id),
#                 'low_stock_count': self.dashboard_model.get_low_stock_count(self.current_user_shop_id),
#                 'total_value': self.dashboard_model.get_total_inventory_value(self.current_user_shop_id),
#                 'categories': self.dashboard_model.get_inventory_by_category(self.current_user_shop_id)
#             }
#         except Exception as e:
#             print(f"Error getting dashboard summary: {e}")
#             return {}

#     def update_dashboard_from_inventory_change(self, change_type, product_data):
#         """Update dashboard when inventory changes occur"""
#         try:
#             # Refresh relevant dashboard sections when inventory changes
#             if change_type in ['add', 'edit', 'delete']:
#                 self.update_summary_metrics()
#                 self.update_inventory_overview()
#                 self.update_low_stock_warnings()
                
#                 if change_type == 'add':
#                     self.update_recent_activities()
                    
#         except Exception as e:
#             print(f"Error updating dashboard from inventory change: {e}")

#     def _show_error_message(self, message):
#         """Show error message dialog"""
#         msg = QMessageBox()
#         msg.setIcon(QMessageBox.Critical)
#         msg.setText("Dashboard Error")
#         msg.setInformativeText(message)
#         msg.setWindowTitle("Error")
#         msg.exec_()

#     def _show_success_message(self, message):
#         """Show success message dialog"""
#         msg = QMessageBox()
#         msg.setIcon(QMessageBox.Information)
#         msg.setText("Dashboard Success")
#         msg.setInformativeText(message)
#         msg.setWindowTitle("Success")
#         msg.exec_()

#     def _show_info_message(self, message):
#         """Show info message dialog"""
#         msg = QMessageBox()
#         msg.setIcon(QMessageBox.Information)
#         msg.setText("Dashboard Info")
#         msg.setInformativeText(message)
#         msg.setWindowTitle("Information")
#         msg.exec_()