import os

from PyQt6.QtWidgets import QCalendarWidget, QTextEdit
from PyQt6.QtCore import QDate, Qt, QTimer
from PyQt6.QtGui import QIcon

from utils import BASEDIR


# Calendário para selecionar data
class Calendar(QCalendarWidget):
    def __init__(self, parent, txt_parent, window_title):
        super().__init__()

        self.parent = parent
        self.txt_parent: QTextEdit = txt_parent
        self.clicked.connect(self.showDate)

        self.setWindowTitle(window_title)
        self.setWindowIcon(QIcon(os.path.join(BASEDIR, '/assets/calendar-64.png')))
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
        self.setFixedSize(312, 190)

    # Sobrescreve método .show para redimensionar o calendário para o centro da janela principal
    def show(self):
        geo = self.geometry()
        geo.moveCenter(self.parent.geometry().center())
        QTimer.singleShot(0, lambda: self.setGeometry(geo))

        super().show()

    # Insere data selecionada no line_edit passado para a instância e fecha o pop-up
    def showDate(self, date: QDate):
        self.txt_parent.setText(date.toString('dd/MM/yyyy'))
        self.hide()
