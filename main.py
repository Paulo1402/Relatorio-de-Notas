import sys

from PyQt6 import QtGui
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QHeaderView

from services.crud import create, read, update, delete, QueryError
from ui.MainWindow import Ui_MainWindow
from utils.calendar import Calendar
from utils.message import Message
from utils.model import Model
from utils import *


class App(QMainWindow, Ui_MainWindow):
    MODE: Mode = Mode.INSERT
    ID: int = -1

    def __init__(self, parent=None):
        super().__init__(parent)

        self.calendars: dict | None = None
        self.model: Model | None = None

        # Cria popup template para usar ao longo do programa
        self.yes = QMessageBox.StandardButton.Yes
        self.no = QMessageBox.StandardButton.No

        self.message = Message(
            self,
            [
                (self.yes, 'Sim'),
                (self.no, 'Não')
            ]
        )

        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        # Conecta botões do menu nas páginas do stacked widget
        self.bt_register_menu.clicked.connect(lambda: self.mp_main.setCurrentIndex(0))
        self.bt_register_menu.clicked.connect(lambda: self.clear_registry())
        self.bt_search_menu.clicked.connect(lambda: self.mp_main.setCurrentIndex(1))
        self.bt_export_menu.clicked.connect(lambda: self.mp_main.setCurrentIndex(2))

        # Define a primeira página ao abrir o progrma
        self.mp_main.setCurrentIndex(0)

        # Define icon  e título da janela
        self.setWindowIcon(QtGui.QIcon('assets/icons8-tarefa-64.png'))
        self.setWindowTitle('Relatório de Notas')

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

        # Remove valor inicial do ComboBox e alinha ao centro
        self.cb_supplier.setCurrentIndex(-1)
        self.cb_supplier.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Desabilita o botão deletar inicialmente
        self.bt_delete.setDisabled(True)
        self.statusBar.showMessage('Modo: Inserir')
        self.ID = -1

        # self.cb_month.setEditable(True)
        # line_edit = self.cb_month.lineEdit()
        # line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # line_edit.setReadOnly(True)

        # Salva calendários na memória
        self.calendars = {
            "date": Calendar(self, self.txt_date, 'Data'),
            "start_date": Calendar(self, self.txt_start_date, 'Data Inicial'),
            "end_date": Calendar(self, self.txt_end_date, 'Data Final')
        }

        # Configura web view e cria relatório
        self.web_view.setZoomFactor(0.8)
        self.create_report()

        # Carrega fornecedores para ComboBox
        self.load_suppliers()

        # Seta model para list view
        self.model = Model()
        self.table_search.setModel(self.model)
        self.search()

        # Define slots para os botões da página 'Registrar'
        self.bt_save.clicked.connect(self.save_registry)
        self.bt_clear.clicked.connect(self.clear_registry)
        self.bt_delete.clicked.connect(self.delete_registry)

        self.bt_calendar_date.clicked.connect(lambda: self.calendars['date'].show())

        # Define slots para os botões da página 'Pesquisar'
        self.bt_clear_search.clicked.connect(self.clear_search)
        self.bt_search.clicked.connect(self.search)

        self.bt_calendar_start_date.clicked.connect(lambda: self.calendars['start_date'].show())
        self.bt_calendar_end_date.clicked.connect(lambda: self.calendars['end_date'].show())

        self.table_search.doubleClicked.connect(self.history_record_selected)

        vertical_header = self.table_search.verticalHeader()
        vertical_header.sectionDoubleClicked.connect(self.history_record_selected)

        # Define slots para os botões da página 'Exportar'
        self.bt_pdf.clicked.connect(self.export_pdf)
        self.bt_print.clicked.connect(self.print_report)

        self.cb_month.currentIndexChanged.connect(lambda: self.create_report())

        # palette = self.cb_supplier.palette()
        # palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor(50, 255, 25))
        # self.cb_month.setPalette(palette)

        # self.txt_date.setInputMask('00/00/0000')
        # self.txt_value.setInputMask('R$ 0,000.00')

    def save_registry(self):
        fields = [
            self.txt_nfe,
            self.txt_date,
            self.cb_supplier,
            self.txt_value
        ]

        empty_fields = get_empty_fields(fields)

        if len(empty_fields) > 0:
            QMessageBox.warning(self, 'ATENÇÃO', 'Preencha os campos obrigatórios!')
            empty_fields[0].setFocus()
            return

        fields = {
            'nfe': fields[0].text(),
            'date': fields[1].text(),
            'supplier': fields[2].text(),
            'value': fields[3].text()
        }

        if self.MODE == Mode.INSERT:
            message = 'Deseja inserir esse registro no banco de dados?'
        else:
            message = 'Deseja editar esse registro no banco de dados?'

        answer = self.message.show_message(
            'ATENÇÃO',
            message,
            QMessageBox.Icon.Warning,
            default_button=self.yes
        )

        if answer == self.no:
            return

        if self.MODE == Mode.INSERT:
            create(table='history', fields=fields)
            message = 'Registro inserido com sucesso.'
        else:
            update(table='history', fields=fields, id_record=self.ID)
            message = 'Registro alterado com sucesso.'

        QMessageBox.information(self, 'AVISO', message)

    def clear_registry(self):
        self.txt_nfe.clear()
        self.txt_date.clear()
        self.cb_supplier.lineEdit().setText('')
        self.txt_value.clear()

        self.statusBar.showMessage('Modo: Inserir')
        self.bt_delete.setDisabled(True)

        self.ID = -1

    def delete_registry(self):
        answer = self.message.show_message(
            'ATENÇÃO',
            'Deseja deletar esse registro no banco de dados?',
            QMessageBox.Icon.Warning,
            default_button=self.no
        )

        if answer == self.no:
            return

        delete(table='history', id_record=self.ID)

    def clear_search(self):
        self.txt_start_date.clear()
        self.txt_end_date.clear()
        self.txt_supplier_search.clear()
        self.txt_nfe_search.clear()

    def search(self):
        nfe = self.txt_nfe_search.text()
        supplier = self.txt_supplier_search.text()
        start_date = parse_date(self.txt_start_date.text(), '%d/%m/%Y', '%Y-%m-%d', on_fail=DateMinMax.MIN)
        end_date = parse_date(self.txt_end_date.text(), '%d/%m/%Y', '%Y-%m-%d', on_fail=DateMinMax.MAX)

        try:
            query = read(
                table='history',
                fields=['id', 'nfe', 'date', 'supplier', 'value'],
                where={
                    'clause': "WHERE nfe LIKE '%' || ? ||  '%' AND supplier LIKE '%' || ? || '%' AND date >= ? AND "
                              "date <= ?",
                    'values': [nfe, supplier, start_date, end_date]
                }
            )
            self.model.setQuery(query)

            self.model.setHeaderData(1, Qt.Orientation.Horizontal, 'NFE')
            self.model.setHeaderData(2, Qt.Orientation.Horizontal, 'DATA')
            self.model.setHeaderData(3, Qt.Orientation.Horizontal, 'FORNECEDOR')
            self.model.setHeaderData(4, Qt.Orientation.Horizontal, 'VALOR')

            self.table_search.setColumnHidden(0, True)
            self.table_search.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        except QueryError as e:
            QMessageBox.critical(
                self,
                'CRÍTICO',
                f'Não foi possível realizar a consulta, verifique a query.\n\n{e.query}'
            )

    def export_pdf(self):
        answer = self.message.show_message(
            'PERGUNTA',
            'Deseja exportar o relatório em pdf?',
            QMessageBox.Icon.Question,
            default_button=self.yes
        )

        if answer == self.no:
            return

        path = QFileDialog.getSaveFileName(self.centralwidget, 'Salvar em PDF.')

        if path:
            self.web_view.printToPdf(path)

    def print_report(self):
        answer = self.message.show_message(
            'PERGUNTA',
            'Deseja imprimir o relátorio?',
            QMessageBox.Icon.Question,
            default_button=self.yes
        )

        if answer == self.no:
            return

        # self.web_view.print()

    def history_record_selected(self, index: QModelIndex | int):
        row = index.row() if isinstance(index, QModelIndex) else index

        id_record = self.model.index(row, 0).data()
        nfe = self.model.index(row, 1).data()
        date = self.model.index(row, 2).data()
        supplier = self.model.index(row, 3).data()
        value = self.model.index(row, 4).data()

        self.txt_nfe.setText(nfe)
        self.txt_date.setText(date)
        self.cb_supplier.lineEdit().setText(supplier)
        self.txt_value.setText(value)

        self.MODE = Mode.UPDATE
        self.ID = id_record

        self.bt_delete.setDisabled(False)

        self.mp_main.setCurrentIndex(0)
        self.statusBar.showMessage(f'Modo: Editar | ID: {id_record}')

    def load_suppliers(self):
        query = read(
            'suppliers',
            fields=['supplier'],
            where={
                'clause': '',
                'values': []
            }
        )

        data = []
        query.first()

        while query.next():
            data.append(query.value(0))

        self.cb_supplier.clear()
        self.cb_supplier.addItems(data)

    def create_report(self):
        month_name = self.cb_month.currentText()
        month_ref = self.cb_month.currentIndex() + 1
        start_date, end_date = parse_month(month_ref)

        rows = []
        total = 0

        queue = read(
            'history',
            fields=['nfe', 'date', 'supplier', 'value'],
            where={
                'clause': "WHERE date >= ? AND date <= ?",
                'values': [start_date, end_date]
            }
        )

        queue.first()

        while queue.next():
            nfe = queue.value(0)
            date = queue.value(1)
            supplier = queue.value(2)
            value = queue.value(3)

            rows.append({
                'nfe': nfe,
                'date': parse_date(date, input_format='%Y-%m-%d', output_format='%d/%b'),
                'supplier': supplier,
                'value': from_float_to_currency(value)
            })

            total += value

        data = {
            'rows': rows,
            'total': from_float_to_currency(total),
            'year': 2023,
            'month': month_name
        }

        html = create_html(data)
        self.web_view.setHtml(html)


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
