from PySide6.QtWidgets import QDialog, QComboBox
from PySide6.QtCore import QPoint, QEvent, Qt
from PySide6.QtGui import QAction

from ui.CalendarDialog import Ui_Dialog


class CalendarDialog(QDialog, Ui_Dialog):
    """Diálogo para escolher datas através de uma interface"""

    def __init__(self, parent, txt_parent):
        super().__init__(parent)
        self.setupUi(self)

        self.txt_parent: QComboBox = txt_parent

        # Remove cabeçalho da janela
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # Seta a posição do popup relativo ao txt_parent
        point = self.txt_parent.mapToGlobal(QPoint(0, 0))
        self.setGeometry(point.x(), point.y() + self.txt_parent.height(), 275, 192)

        # Vincula handle ao evento click
        self.calendar.clicked.connect(self.set_date)

        # Cria action e seta shortcuts do teclado
        shortcut = QAction('shortcut', self)
        shortcut.setShortcuts(['enter', 'return', 'space'])
        shortcut.triggered.connect(self.set_date)

        # Seta action ao diálogo
        self.addAction(shortcut)

    def changeEvent(self, event: QEvent) -> None:
        """Fecha diálogo caso perca o foco"""
        if not self.isActiveWindow():
            self.close()

    def set_date(self):
        """Seta data ao txt vinculado a classe e encerra o diálogo"""
        date = self.calendar.selectedDate()

        self.txt_parent.lineEdit().setText(date.toString('dd/MM/yyyy'))
        self.close()
