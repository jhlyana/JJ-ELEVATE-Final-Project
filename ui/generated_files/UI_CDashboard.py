# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/raw_files/UI_CDashboard.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CASHIER_DASHBOARD(object):
    def setupUi(self, CASHIER_DASHBOARD):
        CASHIER_DASHBOARD.setObjectName("CASHIER_DASHBOARD")
        CASHIER_DASHBOARD.resize(1921, 1005)
        CASHIER_DASHBOARD.setStyleSheet("background: white;")
        self.frame_45 = QtWidgets.QFrame(CASHIER_DASHBOARD)
        self.frame_45.setGeometry(QtCore.QRect(300, 0, 1621, 211))
        self.frame_45.setStyleSheet("background:transparent;")
        self.frame_45.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_45.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_45.setObjectName("frame_45")
        self.timeLabel = QtWidgets.QLabel(self.frame_45)
        self.timeLabel.setGeometry(QtCore.QRect(840, 20, 731, 171))
        font = QtGui.QFont()
        font.setFamily("Montserrat ExtraBold")
        font.setPointSize(38)
        font.setBold(True)
        font.setWeight(75)
        self.timeLabel.setFont(font)
        self.timeLabel.setStyleSheet("\n"
"    background-color: #f6f3ee;\n"
"    border-radius: 16;\n"
"    padding: 10px;\n"
"color: #051a54;\n"
"")
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.dateLabel = QtWidgets.QLabel(self.frame_45)
        self.dateLabel.setGeometry(QtCore.QRect(40, 20, 771, 171))
        font = QtGui.QFont()
        font.setFamily("Montserrat ExtraBold")
        font.setBold(True)
        font.setWeight(75)
        self.dateLabel.setFont(font)
        self.dateLabel.setStyleSheet("\n"
"    background-color: #f6f3ee;\n"
"    border-radius: 16;\n"
"    padding: 10px;\n"
"\n"
"")
        self.dateLabel.setTextFormat(QtCore.Qt.RichText)
        self.dateLabel.setObjectName("dateLabel")
        self.frame_46 = QtWidgets.QFrame(CASHIER_DASHBOARD)
        self.frame_46.setGeometry(QtCore.QRect(340, 210, 1531, 761))
        self.frame_46.setStyleSheet("\n"
"    background-color: #f6f3ee;\n"
"    border-radius: 16;\n"
"    padding: 10px;\n"
"\n"
"")
        self.frame_46.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_46.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_46.setObjectName("frame_46")
        self.Todays_Sales_box = QtWidgets.QFrame(self.frame_46)
        self.Todays_Sales_box.setGeometry(QtCore.QRect(20, 20, 491, 221))
        self.Todays_Sales_box.setStyleSheet("#salesbox\n"
"{\n"
"border: 1px solid black;\n"
"border-radius: 10px;\n"
"    background-color: white;\n"
"    border: 2px solid black;\n"
"    padding: 10px;\n"
"}")
        self.Todays_Sales_box.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Todays_Sales_box.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Todays_Sales_box.setObjectName("Todays_Sales_box")
        self.salesbox = QtWidgets.QLabel(self.Todays_Sales_box)
        self.salesbox.setGeometry(QtCore.QRect(14, 5, 471, 201))
        self.salesbox.setStyleSheet("\n"
"    background-color: #374550;\n"
"    border-radius: 25;\n"
"    padding: 10px;\n"
"\n"
"")
        self.salesbox.setText("")
        self.salesbox.setObjectName("salesbox")
        self.label_4 = QtWidgets.QLabel(self.Todays_Sales_box)
        self.label_4.setGeometry(QtCore.QRect(150, 120, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: #ffffff;\n"
"background: transparent;")
        self.label_4.setObjectName("label_4")
        self.value_Tod_sales = QtWidgets.QLabel(self.Todays_Sales_box)
        self.value_Tod_sales.setGeometry(QtCore.QRect(70, 30, 361, 111))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        self.value_Tod_sales.setFont(font)
        self.value_Tod_sales.setStyleSheet("color:#ebe0cc;\n"
"background: transparent;\n"
"")
        self.value_Tod_sales.setAlignment(QtCore.Qt.AlignCenter)
        self.value_Tod_sales.setObjectName("value_Tod_sales")
        self.Todays_total_orders_box = QtWidgets.QFrame(self.frame_46)
        self.Todays_total_orders_box.setGeometry(QtCore.QRect(40, 270, 471, 211))
        self.Todays_total_orders_box.setStyleSheet("#ordersbox\n"
"{\n"
"border: 1px solid black;\n"
"border-radius: 10px;\n"
"}")
        self.Todays_total_orders_box.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Todays_total_orders_box.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Todays_total_orders_box.setObjectName("Todays_total_orders_box")
        self.ordersbox = QtWidgets.QLabel(self.Todays_total_orders_box)
        self.ordersbox.setGeometry(QtCore.QRect(0, 0, 461, 191))
        self.ordersbox.setStyleSheet("\n"
"    background-color: #c25b55;\n"
"    border-radius: 25;\n"
"    padding: 10px;\n"
"\n"
"")
        self.ordersbox.setText("")
        self.ordersbox.setObjectName("ordersbox")
        self.value_Tod_orders = QtWidgets.QLabel(self.Todays_total_orders_box)
        self.value_Tod_orders.setGeometry(QtCore.QRect(100, 20, 261, 111))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.value_Tod_orders.setFont(font)
        self.value_Tod_orders.setStyleSheet("color: #ebe0cc;\n"
"background: transparent;")
        self.value_Tod_orders.setAlignment(QtCore.Qt.AlignCenter)
        self.value_Tod_orders.setObjectName("value_Tod_orders")
        self.label_8 = QtWidgets.QLabel(self.Todays_total_orders_box)
        self.label_8.setGeometry(QtCore.QRect(100, 100, 271, 71))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: #ffffff;\n"
"background: transparent;")
        self.label_8.setObjectName("label_8")
        self.Todays_revenue_box = QtWidgets.QFrame(self.frame_46)
        self.Todays_revenue_box.setGeometry(QtCore.QRect(30, 510, 491, 211))
        self.Todays_revenue_box.setStyleSheet("#revenue\n"
"{\n"
"border: 1px solid black;\n"
"border-radius: 10px;\n"
"}")
        self.Todays_revenue_box.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Todays_revenue_box.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Todays_revenue_box.setObjectName("Todays_revenue_box")
        self.revenuebox = QtWidgets.QLabel(self.Todays_revenue_box)
        self.revenuebox.setGeometry(QtCore.QRect(10, 0, 471, 191))
        self.revenuebox.setStyleSheet("\n"
"    background-color: #374550;\n"
"    border-radius: 25;\n"
"    padding: 10px;\n"
"\n"
"")
        self.revenuebox.setText("")
        self.revenuebox.setObjectName("revenuebox")
        self.value_Tod_revenue = QtWidgets.QLabel(self.Todays_revenue_box)
        self.value_Tod_revenue.setGeometry(QtCore.QRect(70, 20, 361, 101))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(32)
        font.setBold(False)
        font.setWeight(50)
        self.value_Tod_revenue.setFont(font)
        self.value_Tod_revenue.setStyleSheet("color:#ebe0cc;\n"
"background: transparent;\n"
"")
        self.value_Tod_revenue.setAlignment(QtCore.Qt.AlignCenter)
        self.value_Tod_revenue.setObjectName("value_Tod_revenue")
        self.label_9 = QtWidgets.QLabel(self.Todays_revenue_box)
        self.label_9.setGeometry(QtCore.QRect(130, 90, 311, 91))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: #ffffff;\n"
"background: transparent;")
        self.label_9.setObjectName("label_9")
        self.dashboard_bestsellers_box = QtWidgets.QFrame(self.frame_46)
        self.dashboard_bestsellers_box.setGeometry(QtCore.QRect(570, 30, 931, 621))
        self.dashboard_bestsellers_box.setStyleSheet("#chartd\n"
"{\n"
"border: 1px solid black;\n"
"border-radius: 10px;\n"
"}")
        self.dashboard_bestsellers_box.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dashboard_bestsellers_box.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dashboard_bestsellers_box.setObjectName("dashboard_bestsellers_box")
        self.frameBestSellersChart = QtWidgets.QFrame(self.dashboard_bestsellers_box)
        self.frameBestSellersChart.setGeometry(QtCore.QRect(20, 80, 881, 511))
        self.frameBestSellersChart.setStyleSheet("background-color: transparent;\n"
"")
        self.frameBestSellersChart.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBestSellersChart.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBestSellersChart.setObjectName("frameBestSellersChart")
        self.bestsellersbox = QtWidgets.QLabel(self.dashboard_bestsellers_box)
        self.bestsellersbox.setGeometry(QtCore.QRect(0, 0, 921, 611))
        self.bestsellersbox.setStyleSheet("\n"
"    background-color: transparent;\n"
"    border-radius: 25;\n"
"    padding: 10px;\n"
"\n"
"    border: 2px solid #b2423c;\n"
"\n"
"")
        self.bestsellersbox.setText("")
        self.bestsellersbox.setObjectName("bestsellersbox")
        self.label_10 = QtWidgets.QLabel(self.dashboard_bestsellers_box)
        self.label_10.setGeometry(QtCore.QRect(270, 10, 461, 101))
        font = QtGui.QFont()
        font.setFamily("Montserrat ExtraBold")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: #201f1d;\n"
"background: transparent;")
        self.label_10.setObjectName("label_10")
        self.bestsellersbox.raise_()
        self.label_10.raise_()
        self.frameBestSellersChart.raise_()
        self.btnViewSalesReport = QtWidgets.QPushButton(self.frame_46)
        self.btnViewSalesReport.setGeometry(QtCore.QRect(650, 660, 371, 61))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(16)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.btnViewSalesReport.setFont(font)
        self.btnViewSalesReport.setStyleSheet("QPushButton {\n"
"    background-color: #022162;\n"
"    border-radius: 10px;  \n"
"    color: #ebe0cc;\n"
"    padding: 2px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(2, 33, 98, 0.9);\n"
"}")
        self.btnViewSalesReport.setObjectName("btnViewSalesReport")
        self.btnProcess_Order = QtWidgets.QPushButton(self.frame_46)
        self.btnProcess_Order.setGeometry(QtCore.QRect(1070, 660, 341, 61))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(16)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.btnProcess_Order.setFont(font)
        self.btnProcess_Order.setStyleSheet("QPushButton {\n"
"    background-color: #374550;\n"
"    border-radius: 10px;  \n"
"    color: #ebe0cc;\n"
"    padding: 2px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(55, 69, 80, 0.9);\n"
"}")
        self.btnProcess_Order.setObjectName("btnProcess_Order")
        self.LeftMenuBar = QtWidgets.QFrame(CASHIER_DASHBOARD)
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

        self.retranslateUi(CASHIER_DASHBOARD)
        QtCore.QMetaObject.connectSlotsByName(CASHIER_DASHBOARD)

    def retranslateUi(self, CASHIER_DASHBOARD):
        _translate = QtCore.QCoreApplication.translate
        CASHIER_DASHBOARD.setWindowTitle(_translate("CASHIER_DASHBOARD", "Form"))
        self.timeLabel.setText(_translate("CASHIER_DASHBOARD", " 09 : 10 : 54 AM"))
        self.dateLabel.setText(_translate("CASHIER_DASHBOARD", "<html><head/><body><p align=\"center\"><span style=\" font-size:38pt; color:#022162;\">March 1, 2025</span><br/><span style=\" font-size:20pt; color:#b2423c;\">Monday</span></p></body></html>"))
        self.label_4.setText(_translate("CASHIER_DASHBOARD", "Today’s Sales"))
        self.value_Tod_sales.setText(_translate("CASHIER_DASHBOARD", "800,000"))
        self.value_Tod_orders.setText(_translate("CASHIER_DASHBOARD", "300"))
        self.label_8.setText(_translate("CASHIER_DASHBOARD", "Today’s Total Orders"))
        self.value_Tod_revenue.setText(_translate("CASHIER_DASHBOARD", "900,000"))
        self.label_9.setText(_translate("CASHIER_DASHBOARD", "Today’s Revenue"))
        self.label_10.setText(_translate("CASHIER_DASHBOARD", "Best Sellers"))
        self.btnViewSalesReport.setText(_translate("CASHIER_DASHBOARD", "View Sales Report"))
        self.btnProcess_Order.setText(_translate("CASHIER_DASHBOARD", "Process Order"))
        self.JJelevate_text_2.setText(_translate("CASHIER_DASHBOARD", "J&J "))
        self.pushButton_Dashboard.setText(_translate("CASHIER_DASHBOARD", "  Home   "))
        self.pushButton_Order_History.setText(_translate("CASHIER_DASHBOARD", "Order History"))
        self.pushButton_Sales.setText(_translate("CASHIER_DASHBOARD", "  Sales"))
        self.pushButton_Account.setText(_translate("CASHIER_DASHBOARD", " Account     "))
        self.pushButton_LogOut.setText(_translate("CASHIER_DASHBOARD", "   Log out"))
        self.JJelevate_text_3.setText(_translate("CASHIER_DASHBOARD", "Elevate"))
        self.pushButton_Orders.setText(_translate("CASHIER_DASHBOARD", " Orders"))
