# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/raw_files/UI_CSales.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CASHIER_SALES(object):
    def setupUi(self, CASHIER_SALES):
        CASHIER_SALES.setObjectName("CASHIER_SALES")
        CASHIER_SALES.resize(1921, 1005)
        CASHIER_SALES.setStyleSheet("background: white;")
        self.sales_inview = QtWidgets.QWidget(CASHIER_SALES)
        self.sales_inview.setGeometry(QtCore.QRect(300, 0, 1931, 1005))
        self.sales_inview.setObjectName("sales_inview")
        self.frame_45 = QtWidgets.QFrame(self.sales_inview)
        self.frame_45.setGeometry(QtCore.QRect(0, 0, 1621, 211))
        self.frame_45.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_45.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_45.setObjectName("frame_45")
        self.comboBox_filterSales = QtWidgets.QComboBox(self.frame_45)
        self.comboBox_filterSales.setGeometry(QtCore.QRect(1350, 50, 231, 71))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.comboBox_filterSales.setFont(font)
        self.comboBox_filterSales.setStyleSheet("    background-color: #ebe0cc;\n"
"    border-radius: 15px;\n"
"font-size:28px;\n"
"text-align: center;")
        self.comboBox_filterSales.setObjectName("comboBox_filterSales")
        self.comboBox_filterSales.addItem("")
        self.comboBox_filterSales.addItem("")
        self.comboBox_filterSales.addItem("")
        self.comboBox_filterSales.addItem("")
        self.comboBox_filterSales.addItem("")
        self.frame_29 = QtWidgets.QFrame(self.frame_45)
        self.frame_29.setGeometry(QtCore.QRect(50, 150, 661, 61))
        self.frame_29.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_29.setObjectName("frame_29")
        self.pushButton_summaryView = QtWidgets.QPushButton(self.frame_29)
        self.pushButton_summaryView.setGeometry(QtCore.QRect(0, 10, 261, 61))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(9)
        self.pushButton_summaryView.setFont(font)
        self.pushButton_summaryView.setStyleSheet("/* Default Button Style */\n"
"QPushButton {\n"
"    background-color: #003366;\n"
"    border-radius: 10px;\n"
"    font-size: 24px;\n"
"    color: #ffffff;\n"
"    padding: 9px;\n"
"    font-family: \"Verdana\", sans-serif;\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* Hover Effect */\n"
"QPushButton:hover {\n"
"    background-color: #8d2721;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"/* Active Button (using CLASS selector) */\n"
"QPushButton.activeButton {\n"
"    background-color: #8d2721;\n"
"    color: #ffffff;\n"
"}")
        self.pushButton_summaryView.setObjectName("pushButton_summaryView")
        self.pushButton_salesDetail = QtWidgets.QPushButton(self.frame_29)
        self.pushButton_salesDetail.setGeometry(QtCore.QRect(260, 10, 281, 61))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(9)
        self.pushButton_salesDetail.setFont(font)
        self.pushButton_salesDetail.setStyleSheet("/* Default Button Style */\n"
"QPushButton {\n"
"    background-color: #003366;\n"
"    border-radius: 10px;\n"
"    font-size: 24px;\n"
"    color: #ffffff;\n"
"    padding: 9px;\n"
"    font-family: \"Verdana\", sans-serif;\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* Hover Effect */\n"
"QPushButton:hover {\n"
"    background-color: #8d2721;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"/* Active Button (using CLASS selector) */\n"
"QPushButton.activeButton {\n"
"    background-color: #8d2721;\n"
"    color: #ffffff;\n"
"}")
        self.pushButton_salesDetail.setObjectName("pushButton_salesDetail")
        self.SALES_label = QtWidgets.QLabel(self.frame_45)
        self.SALES_label.setGeometry(QtCore.QRect(60, 50, 801, 71))
        self.SALES_label.setStyleSheet("color: #12245c;\n"
"font-family: \"Arial Black\", Arial, sans-serif; \n"
"background: transparent;\n"
"font-size: 50px;")
        self.SALES_label.setObjectName("SALES_label")
        self.stackedWidget_Sales = QtWidgets.QStackedWidget(self.sales_inview)
        self.stackedWidget_Sales.setGeometry(QtCore.QRect(0, 210, 1621, 771))
        self.stackedWidget_Sales.setObjectName("stackedWidget_Sales")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.tableWidget_salesSummary = QtWidgets.QTableWidget(self.page)
        self.tableWidget_salesSummary.setGeometry(QtCore.QRect(50, 0, 1531, 741))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.tableWidget_salesSummary.setFont(font)
        self.tableWidget_salesSummary.setStyleSheet(" \n"
"QTableWidget {\n"
"    background-color: white;\n"
"    gridline-color: lightgray;\n"
"    selection-background-color: #ebe0cc;\n"
"    selection-color: white;               /* selected row text */\n"
"}\n"
"\n"
"QTableWidget::item:hover {\n"
"    background-color: #b33c35;  /* slightly lighter hover effect */\n"
"    color: white;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #c25b55; /* deep maroon header */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    padding: 4px;\n"
"    border: 1px solid lightgray;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    padding-left: 12px;\n"
"    padding-right: 12px;\n"
"}")
        self.tableWidget_salesSummary.setObjectName("tableWidget_salesSummary")
        self.tableWidget_salesSummary.setColumnCount(5)
        self.tableWidget_salesSummary.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_salesSummary.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_salesSummary.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_salesSummary.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_salesSummary.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_salesSummary.setHorizontalHeaderItem(4, item)
        self.tableWidget_salesSummary.horizontalHeader().setDefaultSectionSize(310)
        self.stackedWidget_Sales.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.tableWidget_orderDetails = QtWidgets.QTableWidget(self.page_2)
        self.tableWidget_orderDetails.setGeometry(QtCore.QRect(50, 0, 1531, 741))
        self.tableWidget_orderDetails.setStyleSheet(" \n"
"QTableWidget {\n"
"    background-color: white;\n"
"    gridline-color: lightgray;\n"
"    selection-background-color: #ebe0cc;\n"
"    selection-color: white;               /* selected row text */\n"
"}\n"
"\n"
"QTableWidget::item:hover {\n"
"    background-color: #b33c35;  /* slightly lighter hover effect */\n"
"    color: white;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #c25b55; /* deep maroon header */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    padding: 4px;\n"
"    border: 1px solid lightgray;\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    padding-left: 12px;\n"
"    padding-right: 12px;\n"
"}")
        self.tableWidget_orderDetails.setObjectName("tableWidget_orderDetails")
        self.tableWidget_orderDetails.setColumnCount(5)
        self.tableWidget_orderDetails.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_orderDetails.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_orderDetails.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_orderDetails.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orderDetails.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orderDetails.setHorizontalHeaderItem(4, item)
        self.tableWidget_orderDetails.horizontalHeader().setDefaultSectionSize(310)
        self.stackedWidget_Sales.addWidget(self.page_2)
        self.LeftMenuBar = QtWidgets.QFrame(CASHIER_SALES)
        self.LeftMenuBar.setGeometry(QtCore.QRect(0, 0, 301, 1011))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.LeftMenuBar.setFont(font)
        self.LeftMenuBar.setStyleSheet("background-color: rgba(235, 224, 204, 0.47); /* #ebe0cc with 47% opacity */")
        self.LeftMenuBar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LeftMenuBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LeftMenuBar.setObjectName("LeftMenuBar")
        self.JJelevate_text_2 = QtWidgets.QLabel(self.LeftMenuBar)
        self.JJelevate_text_2.setGeometry(QtCore.QRect(60, 220, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.JJelevate_text_2.setFont(font)
        self.JJelevate_text_2.setStyleSheet("color: #12245c;\n"
"font-family: \"Arial Black\", Arial, sans-serif; \n"
"background: transparent;\n"
"font-size: 30px;")
        self.JJelevate_text_2.setScaledContents(True)
        self.JJelevate_text_2.setObjectName("JJelevate_text_2")
        self.Logo = QtWidgets.QLabel(self.LeftMenuBar)
        self.Logo.setGeometry(QtCore.QRect(30, 50, 241, 171))
        self.Logo.setStyleSheet("background: transparent;")
        self.Logo.setText("")
        self.Logo.setPixmap(QtGui.QPixmap("ui/raw_files\\../resources/images/JJLOGO.png"))
        self.Logo.setScaledContents(True)
        self.Logo.setAlignment(QtCore.Qt.AlignCenter)
        self.Logo.setObjectName("Logo")
        self.pushButton_Dashboard = QtWidgets.QPushButton(self.LeftMenuBar)
        self.pushButton_Dashboard.setGeometry(QtCore.QRect(30, 310, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_Dashboard.setFont(font)
        self.pushButton_Dashboard.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border-radius: 25px;\n"
"    padding: 9px;\n"
"    text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"QPushButton.activeButton {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/raw_files\\../resources/images/dashboard_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Dashboard.setIcon(icon)
        self.pushButton_Dashboard.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_Dashboard.setObjectName("pushButton_Dashboard")
        self.pushButton_Order_History = QtWidgets.QPushButton(self.LeftMenuBar)
        self.pushButton_Order_History.setGeometry(QtCore.QRect(30, 470, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(12)
        self.pushButton_Order_History.setFont(font)
        self.pushButton_Order_History.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border-radius: 25px;\n"
"    padding: 9px;\n"
"    text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"QPushButton.activeButton {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ui/raw_files\\../resources/images/inventory_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Order_History.setIcon(icon1)
        self.pushButton_Order_History.setIconSize(QtCore.QSize(46, 42))
        self.pushButton_Order_History.setObjectName("pushButton_Order_History")
        self.pushButton_Sales = QtWidgets.QPushButton(self.LeftMenuBar)
        self.pushButton_Sales.setGeometry(QtCore.QRect(30, 550, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(12)
        self.pushButton_Sales.setFont(font)
        self.pushButton_Sales.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border-radius: 25px;\n"
"    padding: 9px;\n"
"    text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"QPushButton.activeButton {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ui/raw_files\\../resources/images/sales_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Sales.setIcon(icon2)
        self.pushButton_Sales.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_Sales.setObjectName("pushButton_Sales")
        self.pushButton_Account = QtWidgets.QPushButton(self.LeftMenuBar)
        self.pushButton_Account.setGeometry(QtCore.QRect(30, 630, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(12)
        self.pushButton_Account.setFont(font)
        self.pushButton_Account.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border-radius: 25px;\n"
"    padding: 9px;\n"
"    text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"QPushButton.activeButton {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ui/raw_files\\../resources/images/account_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Account.setIcon(icon3)
        self.pushButton_Account.setIconSize(QtCore.QSize(48, 48))
        self.pushButton_Account.setObjectName("pushButton_Account")
        self.pushButton_LogOut = QtWidgets.QPushButton(self.LeftMenuBar)
        self.pushButton_LogOut.setGeometry(QtCore.QRect(30, 890, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(87)
        self.pushButton_LogOut.setFont(font)
        self.pushButton_LogOut.setStyleSheet("QPushButton {\n"
"    background-color:#022162;\n"
"color:white;\n"
"font-weight: 700;\n"
"    border-radius: 25px;\n"
"    padding: 9px;\n"
"font-size: 14;\n"
"text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"        background-color: rgba(2, 33, 98, 0.8);\n"
"        color: white;\n"
"    font-weight: 700;\n"
"}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("ui/raw_files\\../resources/images/WHITElogout_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_LogOut.setIcon(icon4)
        self.pushButton_LogOut.setIconSize(QtCore.QSize(38, 38))
        self.pushButton_LogOut.setObjectName("pushButton_LogOut")
        self.JJelevate_text_3 = QtWidgets.QLabel(self.LeftMenuBar)
        self.JJelevate_text_3.setGeometry(QtCore.QRect(130, 220, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.JJelevate_text_3.setFont(font)
        self.JJelevate_text_3.setStyleSheet("color: #d75413;\n"
"font-family: \"Arial Black\", Arial, sans-serif; \n"
"background: transparent;\n"
"font-size: 29px;\n"
"")
        self.JJelevate_text_3.setScaledContents(True)
        self.JJelevate_text_3.setObjectName("JJelevate_text_3")
        self.pushButton_Orders = QtWidgets.QPushButton(self.LeftMenuBar)
        self.pushButton_Orders.setGeometry(QtCore.QRect(30, 390, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(12)
        self.pushButton_Orders.setFont(font)
        self.pushButton_Orders.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border-radius: 25px;\n"
"    padding: 9px;\n"
"    text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"QPushButton.activeButton {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("ui/raw_files\\../resources/images/orders_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Orders.setIcon(icon5)
        self.pushButton_Orders.setIconSize(QtCore.QSize(46, 42))
        self.pushButton_Orders.setObjectName("pushButton_Orders")

        self.retranslateUi(CASHIER_SALES)
        self.stackedWidget_Sales.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(CASHIER_SALES)

    def retranslateUi(self, CASHIER_SALES):
        _translate = QtCore.QCoreApplication.translate
        CASHIER_SALES.setWindowTitle(_translate("CASHIER_SALES", "Form"))
        self.comboBox_filterSales.setCurrentText(_translate("CASHIER_SALES", "    Filter Sales"))
        self.comboBox_filterSales.setItemText(0, _translate("CASHIER_SALES", "    Filter Sales"))
        self.comboBox_filterSales.setItemText(1, _translate("CASHIER_SALES", "Daily"))
        self.comboBox_filterSales.setItemText(2, _translate("CASHIER_SALES", "Weekly"))
        self.comboBox_filterSales.setItemText(3, _translate("CASHIER_SALES", "Monthly"))
        self.comboBox_filterSales.setItemText(4, _translate("CASHIER_SALES", "All "))
        self.pushButton_summaryView.setText(_translate("CASHIER_SALES", "Summary View"))
        self.pushButton_salesDetail.setText(_translate("CASHIER_SALES", "Detailed View"))
        self.SALES_label.setText(_translate("CASHIER_SALES", "Sales Report"))
        item = self.tableWidget_salesSummary.horizontalHeaderItem(0)
        item.setText(_translate("CASHIER_SALES", "Report ID"))
        item = self.tableWidget_salesSummary.horizontalHeaderItem(1)
        item.setText(_translate("CASHIER_SALES", "Shop Branch"))
        item = self.tableWidget_salesSummary.horizontalHeaderItem(2)
        item.setText(_translate("CASHIER_SALES", "Total Quantity Sold"))
        item = self.tableWidget_salesSummary.horizontalHeaderItem(3)
        item.setText(_translate("CASHIER_SALES", "Total Revenue (₱)"))
        item = self.tableWidget_salesSummary.horizontalHeaderItem(4)
        item.setText(_translate("CASHIER_SALES", "Date Generated"))
        item = self.tableWidget_orderDetails.horizontalHeaderItem(0)
        item.setText(_translate("CASHIER_SALES", "Detail ID"))
        item = self.tableWidget_orderDetails.horizontalHeaderItem(1)
        item.setText(_translate("CASHIER_SALES", "Product Name"))
        item = self.tableWidget_orderDetails.horizontalHeaderItem(2)
        item.setText(_translate("CASHIER_SALES", "Quantity Sold"))
        item = self.tableWidget_orderDetails.horizontalHeaderItem(3)
        item.setText(_translate("CASHIER_SALES", "Total Sales Amount (₱)"))
        item = self.tableWidget_orderDetails.horizontalHeaderItem(4)
        item.setText(_translate("CASHIER_SALES", "Date Recorded"))
        self.JJelevate_text_2.setText(_translate("CASHIER_SALES", "J&J "))
        self.pushButton_Dashboard.setText(_translate("CASHIER_SALES", "  Home   "))
        self.pushButton_Order_History.setText(_translate("CASHIER_SALES", "Order History"))
        self.pushButton_Sales.setText(_translate("CASHIER_SALES", "  Sales"))
        self.pushButton_Account.setText(_translate("CASHIER_SALES", " Account     "))
        self.pushButton_LogOut.setText(_translate("CASHIER_SALES", "   Log out"))
        self.JJelevate_text_3.setText(_translate("CASHIER_SALES", "Elevate"))
        self.pushButton_Orders.setText(_translate("CASHIER_SALES", " Orders"))
