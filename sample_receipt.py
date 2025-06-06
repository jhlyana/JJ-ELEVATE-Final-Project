from fpdf import FPDF, XPos, YPos # Added XPos, YPos for explicit positioning
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, QSizeF # Added QSizeF for printer paper size
import os
import datetime # Import datetime to get current date/time for receipt

class ReceiptPrinter:
    def __init__(self, parent=None):
        self.parent = parent

    def generate_and_print_receipt(self, order_data):
        # Define common receipt dimensions (e.g., 80mm thermal paper)
        # 1 inch = 25.4 mm. So 80mm = 80/25.4 inches.
        # Convert to points (1 point = 1/72 inch)
        PAPER_WIDTH_MM = 80
        PAPER_HEIGHT_MM = 200 # Adjust as needed, thermal paper is continuous
        PAPER_WIDTH_PT = PAPER_WIDTH_MM / 25.4 * 72
        # Use an initial page height; fpdf2 will add new pages if content overflows
        INITIAL_PAGE_HEIGHT_PT = PAPER_HEIGHT_MM / 25.4 * 72

        # Define margins for content within the receipt
        # These margins will be applied to the PDF content area
        LEFT_MARGIN = 5 # in points (approx 1.76 mm)
        RIGHT_MARGIN = 5 # in points (approx 1.76 mm)
        
        # Calculate the actual width available for content
        CONTENT_WIDTH_PT = PAPER_WIDTH_PT - LEFT_MARGIN - RIGHT_MARGIN

        # Initialize PDF document
        # Set unit to 'pt' (points) for precise control and format to custom size
        pdf = FPDF(unit="pt", format=(PAPER_WIDTH_PT, INITIAL_PAGE_HEIGHT_PT))
        pdf.add_page()
        
        # Set auto page break. Margin here is the bottom margin for auto-break.
        pdf.set_auto_page_break(auto=True, margin=10) 
        
        # Apply the custom margins to the PDF content area
        pdf.set_left_margin(LEFT_MARGIN)
        pdf.set_right_margin(RIGHT_MARGIN)
        
        # Move the current drawing position (cursor) to the left margin
        pdf.set_x(LEFT_MARGIN)

        # --- Receipt Header ---
        pdf.set_font("Arial", "B", 12)
        # Using 'text' instead of 'txt' and explicit 'new_x', 'new_y' for deprecation warnings
        pdf.cell(w=CONTENT_WIDTH_PT, h=10, text="J&J Elevate", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        pdf.set_font("Arial", "", 8)
        pdf.cell(w=CONTENT_WIDTH_PT, h=5, text="Moalboal, Cebu, Philippines", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(w=CONTENT_WIDTH_PT, h=5, text="VAT Reg. TIN: 123-456-789-000", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(w=CONTENT_WIDTH_PT, h=5, text="-------------------------------------", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2) # Add a line break for spacing

        pdf.set_font("Arial", "B", 10)
        pdf.cell(w=CONTENT_WIDTH_PT, h=7, text="SALES RECEIPT", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        pdf.set_font("Arial", "", 8)
        pdf.cell(w=CONTENT_WIDTH_PT, h=5, text=f"Order ID: {order_data['order_id']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(w=CONTENT_WIDTH_PT, h=5, text=f"Date: {order_data['date']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(w=CONTENT_WIDTH_PT, h=5, text=f"Cashier: {order_data['cashier_name']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(5) # Add a line break for spacing

        # --- Items Header ---
        pdf.set_font("Arial", "B", 8)
        # Define column widths as percentages of the CONTENT_WIDTH_PT
        # Ensure these sum up to 1.0 (or very close)
        COL_ITEM_WIDTH = CONTENT_WIDTH_PT * 0.50  # 50% for item name
        COL_QTY_WIDTH = CONTENT_WIDTH_PT * 0.15   # 15% for quantity
        COL_PRICE_WIDTH = CONTENT_WIDTH_PT * 0.15 # 15% for unit price
        COL_TOTAL_WIDTH = CONTENT_WIDTH_PT * 0.20 # 20% for total price of item

        pdf.cell(w=COL_ITEM_WIDTH, h=7, text="Item", align="L")
        pdf.cell(w=COL_QTY_WIDTH, h=7, text="Qty", align="C")
        pdf.cell(w=COL_PRICE_WIDTH, h=7, text="Price", align="R")
        # Last cell in the row moves to the next line at the left margin
        pdf.cell(w=COL_TOTAL_WIDTH, h=7, text="Total", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Draw a line across the full content width
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + CONTENT_WIDTH_PT, pdf.get_y())
        pdf.ln(2)

        # --- Items List ---
        pdf.set_font("Arial", "", 8)
        for item in order_data['items']:
            # 1. Print Item Name (can be multi-line using multi_cell)
            initial_y_for_row = pdf.get_y() # Store Y before printing item name
            
            # multi_cell automatically wraps text and advances Y position
            pdf.multi_cell(w=COL_ITEM_WIDTH, h=6, text=item['name'], align="L", border=0) 
            
            # Get the Y position after the multi_cell has finished (this is the lowest point for this item row)
            y_after_item_name_multi_cell = pdf.get_y()

            # 2. Print Quantity, Price, and Total on the same logical line as the item name
            # We need to manually set Y back to the initial Y for the row
            pdf.set_y(initial_y_for_row)
            
            # Set X position for Quantity (after item name column, respecting margins)
            pdf.set_x(LEFT_MARGIN + COL_ITEM_WIDTH) 
            pdf.cell(w=COL_QTY_WIDTH, h=6, text=str(item['qty']), align="C") # No new_x/new_y for cells in the middle of a row

            # Set X position for Price (after quantity column)
            pdf.cell(w=COL_PRICE_WIDTH, h=6, text=f"P{item['price']:.2f}", align="R")

            # Set X position for Total (after price column), and move to next line
            pdf.cell(w=COL_TOTAL_WIDTH, h=6, text=f"P{item['total_price']:.2f}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

            # 3. Ensure the cursor for the next item starts after the tallest element in the current row
            # If the multi_cell for the item name made the current Y position lower than where
            # the last cell of Qty/Price/Total ended, we need to advance the Y.
            if pdf.get_y() < y_after_item_name_multi_cell:
                pdf.set_y(y_after_item_name_multi_cell)
            
            pdf.ln(1) # Small spacing between items

        pdf.ln(5) # Spacing before totals
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + CONTENT_WIDTH_PT, pdf.get_y())
        pdf.ln(2)

        # --- Totals ---
        pdf.set_font("Arial", "B", 10)
        # Define column widths for labels and values in the totals section
        COL_TOTAL_LABEL_WIDTH = CONTENT_WIDTH_PT * 0.75 # 75% for labels like SUBTOTAL
        COL_TOTAL_VALUE_WIDTH = CONTENT_WIDTH_PT * 0.25 # 25% for values

        pdf.cell(w=COL_TOTAL_LABEL_WIDTH, h=7, text="SUBTOTAL:", align="R")
        pdf.cell(w=COL_TOTAL_VALUE_WIDTH, h=7, text=f"P{order_data['subtotal']:.2f}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.cell(w=COL_TOTAL_LABEL_WIDTH, h=7, text="VAT (12%):", align="R")
        pdf.cell(w=COL_TOTAL_VALUE_WIDTH, h=7, text=f"P{order_data['vat_amount']:.2f}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.cell(w=COL_TOTAL_LABEL_WIDTH, h=7, text="TOTAL AMOUNT:", align="R")
        pdf.cell(w=COL_TOTAL_VALUE_WIDTH, h=7, text=f"P{order_data['grand_total']:.2f}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.ln(5)

        pdf.cell(w=COL_TOTAL_LABEL_WIDTH, h=7, text="CASH:", align="R")
        pdf.cell(w=COL_TOTAL_VALUE_WIDTH, h=7, text=f"P{order_data['cash_given']:.2f}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.cell(w=COL_TOTAL_LABEL_WIDTH, h=7, text="CHANGE:", align="R")
        pdf.cell(w=COL_TOTAL_VALUE_WIDTH, h=7, text=f"P{order_data['change']:.2f}", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(5)
        pdf.cell(w=CONTENT_WIDTH_PT, h=5, text="-------------------------------------", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # --- Footer ---
        pdf.set_font("Arial", "", 8)
        pdf.cell(w=CONTENT_WIDTH_PT, h=7, text="Thank You for your purchase!", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(w=CONTENT_WIDTH_PT, h=5, text="J&J Elevate Sales Team", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(w=CONTENT_WIDTH_PT, h=5, text="For inquiries: (034) 123-4567", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Save to a temporary file
        temp_pdf_path = "temp_receipt.pdf"
        try:
            pdf.output(temp_pdf_path)
            print(f"Receipt generated at: {os.path.abspath(temp_pdf_path)}")

            # Use PyQt's printing system
            printer = QPrinter(QPrinter.HighResolution)
            
            # Set custom paper size for the printer using QSizeF
            # This is crucial for thermal printers.
            printer.setPaperSize(QSizeF(PAPER_WIDTH_MM, PAPER_HEIGHT_MM), QPrinter.Millimeter)

            dialog = QPrintDialog(printer, self.parent)
            if dialog.exec_() == QPrintDialog.Accepted:
                # Open the PDF with QDesktopServices for printing
                # This relies on the system's default PDF viewer/printer configuration
                QDesktopServices.openUrl(QUrl.fromLocalFile(temp_pdf_path))
                QMessageBox.information(self.parent, "Print Receipt", "Receipt sent to printer.")
            else:
                QMessageBox.warning(self.parent, "Print Cancelled", "Printing cancelled by user.")

        except Exception as e:
            QMessageBox.critical(self.parent, "Error Printing Receipt", f"An error occurred: {e}")
        finally:
            # Clean up temporary file (optional). Keep it for debugging initially.
            if os.path.exists(temp_pdf_path):
                # os.remove(temp_pdf_path) # Uncomment this line in production
                pass


# --- How to integrate this in your main application ---
# You would typically call this after a successful order
# Example usage (run this in your main app, e.g., in a button click handler):
if __name__ == '__main__':
    import sys
    from PyQt5 import QtWidgets, QtCore

    app = QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow() # Your main window instance

    # Sample order data (this would come from your order processing logic)
    # Using datetime to get a dynamic date/time
    current_time = datetime.datetime.now().strftime("%B %d, %Y %H:%M")
    
    sample_order = {
        "order_id": "JJ-20250606-001",
        "date": current_time, # Dynamic date/time
        "cashier_name": "Jhane Doe",
        "items": [
            {"name": "Roof Tile (Red, 1.2mm) - High Quality, Durable, Weather Resistant", "qty": 10, "price": 120.00, "total_price": 1200.00},
            {"name": "Spandrel (White, 0.8mm)", "qty": 5, "price": 85.50, "total_price": 427.50},
            {"name": "Gutter (Gray, 1.0mm) - Long Section, Standard Profile", "qty": 2, "price": 250.00, "total_price": 500.00},
            {"name": "Screws (Galvanized, 2 inch) - Box of 100", "qty": 1, "price": 150.00, "total_price": 150.00},
            {"name": "Sealant (Waterproof, Clear)", "qty": 3, "price": 75.00, "total_price": 225.00}
        ],
        "subtotal": 0.0, # Will be calculated dynamically
        "vat_amount": 0.0, # Will be calculated dynamically
        "grand_total": 0.0, # Will be calculated dynamically
        "cash_given": 2400.00, # Example cash given
        "change": 0.0 # Will be calculated dynamically
    }

    # Calculate totals dynamically for the sample order
    sample_order['subtotal'] = sum(item['total_price'] for item in sample_order['items'])
    VAT_RATE = 0.12
    sample_order['vat_amount'] = sample_order['subtotal'] * VAT_RATE
    sample_order['grand_total'] = sample_order['subtotal'] + sample_order['vat_amount']
    sample_order['change'] = sample_order['cash_given'] - sample_order['grand_total']


    printer = ReceiptPrinter(parent=main_window)
    
    dummy_label = QtWidgets.QLabel("Click 'Print' to generate and print a sample receipt.")
    print_button = QtWidgets.QPushButton("Print Sample Receipt")
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(dummy_label)
    layout.addWidget(print_button)
    central_widget = QtWidgets.QWidget()
    central_widget.setLayout(layout)
    main_window.setCentralWidget(central_widget)

    print_button.clicked.connect(lambda: printer.generate_and_print_receipt(sample_order))
    main_window.show()

    sys.exit(app.exec_())