import sys
import datetime

from PyQt6 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQueryModel

from ui.MainWindow import Ui_MainWindow
from utils.calendar import Calendar
from utils.message import Message
from utils.model import Model
from services.crud import create, read, update, delete, QueryError

MODE = 'INSERT'


class App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.calendars = []

        self.model = None

        # Cria popup template para usar ao longo do programa
        self.yes = QMessageBox.StandardButton.Yes
        self.no = QMessageBox.StandardButton.No

        self.popup = QMessageBox(self)
        self.popup.setStandardButtons(self.yes | self.no)
        self.popup.setDefaultButton(self.yes)

        self.popup.button(self.yes).setText('Sim')
        self.popup.button(self.no).setText('Não')

        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        # Conecta botões do menu nas páginas do stacked widget
        self.bt_register_menu.clicked.connect(lambda: self.mp_main.setCurrentIndex(0))
        self.bt_search_menu.clicked.connect(lambda: self.mp_main.setCurrentIndex(1))
        self.bt_export_menu.clicked.connect(lambda: self.mp_main.setCurrentIndex(2))

        # Define a primeira página ao abrir o progrma
        self.mp_main.setCurrentIndex(0)

        # Define icon da janela
        self.setWindowIcon(QtGui.QIcon('assets/icons8-tarefa-64.png'))

        # Popula Month ComboBox
        self.cb_month.addItems([
            'JANEIRO',
            'FEVEREIRO',
            'MARÇO',
            'ABRIL',
            'MAIO',
            'JUNHO',
            'JULHO',
            'AGOSTO',
            'SETEMBRO',
            'OUTUBRO',
            'NOVEMBRO',
            'DEZEMBRO'
        ])

        self.cb_supplier.setCurrentIndex(-1)
        self.cb_supplier.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)

        # self.cb_month.setEditable(True)
        # line_edit = self.cb_month.lineEdit()
        # line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # line_edit.setReadOnly(True)

        self.calendars = [
            Calendar(self, self.txt_date),
            Calendar(self, self.txt_start_date),
            Calendar(self, self.txt_end_date)
        ]

        self.web_view.setZoomFactor(0.8)

        # Define slots para os botões da página 'Registrar'
        self.bt_save.clicked.connect(self.save_registry)
        self.bt_clear.clicked.connect(self.clear_registry)
        self.bt_delete.clicked.connect(self.delete_registry)

        self.bt_calendar_date.clicked.connect(lambda: self.calendars[0].show())

        # Define slots para os botões da página 'Pesquisar'
        self.bt_clear_search.clicked.connect(self.clear_search)
        self.bt_search.clicked.connect(self.search)

        self.bt_calendar_start_date.clicked.connect(lambda: self.calendars[1].show())
        self.bt_calendar_end_date.clicked.connect(lambda: self.calendars[2].show())

        # Define slots para os botões da página 'Exportar'
        self.bt_pdf.clicked.connect(self.export_pdf)
        self.bt_print.clicked.connect(self.print_report)

        self.cb_month.currentIndexChanged.connect(lambda x: print(x))

        palette = self.cb_supplier.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(50, 255, 25))
        self.cb_month.setPalette(palette)

        # Seta model para list view
        self.model = QSqlQueryModel()
        self.list_search.setModel(self.model)
        self.search()

    def save_registry(self):
        if MODE == 'INSERT':
            # self.popup.setWindowTitle('ATENÇÃO')
            # self.popup.setText('Deseja inserir esse registro no banco de dados?')

            # answer = self.popup.exec()

            message = Message(
                self,
                'ATENÇÃO',
                'Deseja inserir esse registro no banco de dados?',
                QMessageBox.Icon.Warning,
                [(QMessageBox.StandardButton.Yes, 'Sim'), (QMessageBox.StandardButton.No, 'Não')],
                QMessageBox.StandardButton.Yes
            )

            answer = message.exec()

            if answer == self.no:
                return
        else:
            pass

    def clear_registry(self):
        self.txt_nfe.clear()
        self.txt_date.clear()
        self.cb_supplier.clear()
        self.txt_value.clear()

    def delete_registry(self):
        pass

    def clear_search(self):
        self.txt_start_date.clear()
        self.txt_end_date.clear()
        self.txt_supplier_search.clear()
        self.txt_nfe_search.clear()

    def search(self):
        nfe = self.txt_nfe_search.text()
        supplier = self.txt_supplier_search.text()
        start_date = self.txt_start_date.text()
        end_date = self.txt_end_date.text()

        datetime.datetime.strftime()

        try:
            query = read(
                'history',
                [
                    'id',
                    'nfe',
                    'date',
                    'supplier',
                    'price'
                ],
                where="nfe LIKE '%' || ? ||  '%' AND "
                      "supplier LIKE '%' || ? || '%' AND "
                      "date >= ? AND date <= ?"
            )
        except QueryError:
            QMessageBox.critical(self, 'CRÍTICO', 'Não foi possível realizar a consulta!')

        self.model.setQuery(query)

    def export_pdf(self):
        pass

    def print_report(self):
        pass

    def create_report(self):
        with open('utils/templates/report.html', 'r', encoding='utf-8') as f:
            self.web_view.setHtml(f.read())


# Usado para auxiliar na depuração
def exception_hook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)
    sys.exit(1)


# Inicia o aplicativo
if __name__ == "__main__":
    sys.excepthook = exception_hook
    qt = QApplication(sys.argv)
    # qt.setStyle('Fusion')
    app = App()
    app.show()

    sys.exit(qt.exec())
