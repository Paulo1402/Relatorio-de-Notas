from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QDate

from ui.CalendarDialog import Ui_Dialog


class CalendarDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, txt_parent, window_title):
        super().__init__(parent)
        self.setupUi(self)

        self.txt_parent = txt_parent

        self.setWindowTitle(window_title)
        self.setFixedSize(312, 190)
        self.calendar.clicked.connect(self.show_date)

    def show_date(self, date: QDate):
        self.txt_parent.setText(date.toString('dd/MM/yyyy'))
        self.close()
