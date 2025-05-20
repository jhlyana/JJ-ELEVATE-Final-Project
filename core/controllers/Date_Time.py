from PyQt5.QtCore import QDate, QTime, QTimer, Qt
from PyQt5.QtWidgets import QLabel

class DateTimeController:
    def __init__(self):
        self.date_labels = []
        self.time_labels = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_all)
        self.timer.start(1000)  # Update every second

    def add_date_time_labels(self, date_label: QLabel, time_label: QLabel):
        """Register date and time labels to be updated"""
        date_label.setTextFormat(Qt.RichText)
        time_label.setTextFormat(Qt.RichText)
        self.date_labels.append(date_label)
        self.time_labels.append(time_label)
        self.update_all()  # Immediate update

    def update_all(self):
        """Update all registered date and time displays"""
        self.update_date()
        self.update_time()

    def update_date(self):
        """Update all date labels with current date"""
        current_date = QDate.currentDate()
        formatted_date = current_date.toString("MMMM dd, yyyy")
        formatted_day = current_date.toString("dddd")
        
        rich_text = f"""
        <html>
        <head/>
        <body>
            <p align="center">
                <span style="font-size:38pt; color:#022162;">{formatted_date}</span><br/>
                <span style="font-size:20pt; color:#b2423c;">{formatted_day}</span>
            </p>
        </body>
        </html>
        """
        
        for label in self.date_labels:
            label.setText(rich_text)

    def update_time(self):
        """Update all time labels with current time"""
        current_time = QTime.currentTime()
        formatted_time = current_time.toString("hh:mm:ss AP")
        
        for label in self.time_labels:
            label.setText(formatted_time)