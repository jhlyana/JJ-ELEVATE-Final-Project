import logging
# Configure logging (IMPORTANT: Ensure this is at the top of this file)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from core.models.ODashboard_pageModel import DashboardPageModel

class DashboardPageController:
    # Changed cashier_controller to owner_controller to be consistent with OwnerController
    def __init__(self, dashboard_ui, owner_controller): 
        logging.debug("THIS IS THE ODashboard_pageController.py FILE BEING EXECUTED!")
        self.ui = dashboard_ui
        self.owner_controller = owner_controller
        self.current_canvas = None  # Track the current canvas
        
        logging.debug(f"Initializing DashboardPageController for Owner.")
        logging.debug(f"Owner Controller Database: {self.owner_controller.database}")
        logging.debug(f"Owner Controller User ID: {self.owner_controller.current_user_id}")
        logging.debug(f"Owner Controller Shop ID: {self.owner_controller.current_shop_id}")

        self.model = DashboardPageModel(
            self.owner_controller.database,
            self.owner_controller.current_user_id,
            self.owner_controller.current_shop_id
        )
        
        # Initialize dashboard data
        self.update_dashboard_data()
        self.add_best_sellers_chart()

    def update_dashboard_data(self):
        """Update all dashboard metrics"""
        logging.debug("Updating dashboard data...")
        # Get today's data
        today_sales = self.model.get_today_sales()
        today_orders = self.model.get_today_orders()
        today_revenue = self.model.get_today_revenue()
        
        logging.debug(f"Today's Sales: {today_sales}")
        logging.debug(f"Today's Orders: {today_orders}")
        logging.debug(f"Today's Revenue: {today_revenue}")
        
        # Ensure the font settings are applied if the UI elements exist
        try:
            font = self.ui.value_Tod_sales.font()
            font.setPointSize(32)
            font.setBold(True)    
            
            # Apply the same font to both sales and revenue
            self.ui.value_Tod_sales.setFont(font)
            self.ui.value_Tod_revenue.setFont(font)
        except AttributeError as e:
            logging.warning(f"Could not set font for dashboard values (UI elements might be missing): {e}")
        
        # Update UI elements
        # Ensure your UI has these exact object names: value_Tod_sales, value_Tod_orders, value_Tod_revenue
        try:
            self.ui.value_Tod_sales.setText(f"₱{today_sales:,.2f}")
            self.ui.value_Tod_orders.setText(f"{today_orders}")
            self.ui.value_Tod_revenue.setText(f"₱{today_revenue:,.2f}")
            logging.debug("Dashboard data updated in UI.")
        except AttributeError as e:
            logging.error(f"Failed to update dashboard UI elements (check object names): {e}")

    def add_best_sellers_chart(self):
        """Add best sellers chart to the dashboard"""
        logging.debug("Attempting to add best sellers chart...")
        
        # Clear existing chart safely
        if self.current_canvas is not None:
            self.current_canvas.deleteLater()
            self.current_canvas = None
            logging.debug("Cleared existing chart canvas.")
        
        # Get the frame's layout or create a new one
        # Ensure your UI has a QFrame named frameBestSellersChart
        try:
            if self.ui.frameBestSellersChart.layout() is None:
                layout = QtWidgets.QVBoxLayout()
                self.ui.frameBestSellersChart.setLayout(layout)
                logging.debug("Created new QVBoxLayout for frameBestSellersChart.")
            else:
                layout = self.ui.frameBestSellersChart.layout()
                # Clear any existing widgets in the layout
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                        logging.debug("Cleared existing widget from frameBestSellersChart layout.")
        except AttributeError as e:
            logging.error(f"Could not access frameBestSellersChart.layout or set layout: {e}")
            return # Exit if the UI frame isn't accessible
    
        # Adjust frame size (optional, might be better handled in Qt Designer)
        # self.ui.frameBestSellersChart.setGeometry(QtCore.QRect(20, 80, 891, 555))
        
        # Create matplotlib figure
        fig = Figure(figsize=(6.5, 4.3), dpi=100, facecolor='none')
        ax = fig.add_subplot(111)
        ax.set_facecolor('none')  # Set axes background to transparent
        
        # Get best sellers data
        best_sellers = self.model.get_best_sellers()
        logging.debug(f"Best Sellers Data retrieved: {best_sellers}")
        
        if not best_sellers:
            ax.text(0.5, 0.5, 'No sales data available', 
                            ha='center', va='center', fontsize=12)
            ax.set_xticks([])
            ax.set_yticks([])
            logging.warning("No best sellers data available. Displaying 'No sales data available'.")
        else:
            items = [row['product_name'] for row in best_sellers]
            sales = [row['total_quantity'] for row in best_sellers]
            
            # Create bar chart
            bars = ax.bar(items, sales, color='#003366', width=0.6)
            logging.debug("Best sellers bar chart created.")
            
            # Customize chart
            ax.set_ylabel('Quantity Sold', fontsize=10)
            ax.tick_params(axis='x', labelsize=8, rotation=45)
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                                f'{int(height)}',
                                ha='center', va='bottom', fontsize=8)
        
        # Adjust spacing
        fig.tight_layout()
      
        # Create canvas and add to layout
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        self.current_canvas = canvas  # Store reference to current canvas
        
        # Set canvas size policy
        canvas.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, 
            QtWidgets.QSizePolicy.Expanding
        )
        logging.debug("Best sellers chart added to dashboard.")