import sys
import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QHeaderView
from PyQt6.QtCore import Qt, QModelIndex, QMarginsF, QRegularExpression
from PyQt6.QtGui import QPageLayout, QIcon, QPageSize, QRegularExpressionValidator, QCloseEvent
from PyQt6.QtPrintSupport import QPrinter

from ui.MainWindow import Ui_MainWindow
from utils.model import Model
from utils.message import Message
from utils.calendar import Calendar
from utils import *
from services import *


# todo Sistema de backup semanal
# todo Menu Action para deletar dados do autocomplete de fornecedor
# todo Menu Action para deletar dados anuais Ex: todos os dados do ano de 2022


# Janela principal
class App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Instancia variáveis
        self.calendars: dict | None = None
        self.model: Model | None = None
        self._ID: int | None = None

        # Cria aliases para botões
        self.yes = QMessageBox.StandardButton.Yes
        self.no = QMessageBox.StandardButton.No

        # Cria template popup
        self.message = Message(self, [(self.yes, 'Sim'), (self.no, 'Não')])

        # Estrutura componentes da ui e em seguida chama a inicialização da janela principal
        self.setupUi(self)
        self.init_ui()

    # Fecha conexão com banco de dados ao fechar o aplicativo
    def closeEvent(self, a0: QCloseEvent) -> None:
        close_connection()
        a0.accept()

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        flag = bool(value + 1)
        message = f'Modo: Editar | ID: {value}' if flag else f'Modo: Registrar'

        self.statusBar.showMessage(message)
        self.bt_delete.setDisabled(not flag)
        self.mp_main.setCurrentIndex(0)
        self.txt_nfe.setFocus()

        self._ID = value

    def init_ui(self):
        # Conecta botões do menu nas páginas do stacked widget
        self.bt_register_menu.clicked.connect(lambda: self.registry_menu_clicked())
        self.bt_search_menu.clicked.connect(lambda: self.search_menu_clicked())
        self.bt_export_menu.clicked.connect(lambda: self.export_menu_clicked())

        # Define icon, título e tamanho da janela
        self.setWindowIcon(QIcon(os.path.join(BASEDIR, 'assets/task-64.png')))
        self.setWindowTitle('Relatório de Notas')
        self.setFixedSize(785, 560)

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

        # Adiciona na ComboBox anos conforme os registros no banco de dados
        years = get_years()
        self.cb_year.addItems(years)

        # Seta ano e mês atual
        current_month, current_year = get_current_month_year()
        self.cb_month.setCurrentIndex(current_month - 1)
        self.cb_year.setCurrentText(str(current_year))

        # Carrega fornecedores para ComboBox
        self.load_suppliers()

        # Remove valor inicial do ComboBox e alinha ao centro
        self.cb_supplier.setCurrentIndex(-1)
        self.cb_supplier.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Salva calendários na memória
        self.calendars = {
            "date": Calendar(self, self.txt_date, 'Data'),
            "start_date": Calendar(self, self.txt_start_date, 'Data Inicial'),
            "end_date": Calendar(self, self.txt_end_date, 'Data Final')
        }

        # Seta model para list view e faz pesquisa
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

        # Define slots para o evento de double click na table view
        self.table_search.doubleClicked.connect(self.history_record_selected)
        self.table_search.verticalHeader().sectionDoubleClicked.connect(self.history_record_selected)

        # Define slots para os botões da página 'Exportar'
        self.bt_pdf.clicked.connect(self.export_pdf)
        self.bt_print.clicked.connect(self.print_report)
        self.cb_month.currentIndexChanged.connect(lambda: self.create_report())
        self.cb_year.currentIndexChanged.connect(lambda: self.create_report())

        # Seta validadores
        validator = QRegularExpressionValidator(
            QRegularExpression(r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[12])/[12][0-9]{3}")
        )
        self.txt_date.setValidator(validator)
        self.txt_start_date.setValidator(validator)
        self.txt_end_date.setValidator(validator)

        validator = QRegularExpressionValidator(QRegularExpression(r'\d+(,\d+)?'))
        self.txt_value.setValidator(validator)

        validator = QRegularExpressionValidator(QRegularExpression(r'\d+'))
        self.txt_nfe_search.setValidator(validator)
        self.txt_nfe.setValidator(validator)

        # Configura web view e cria relatório
        self.web_view.setZoomFactor(0.8)
        self.create_report()

        # Define a primeira página ao abrir o progrma
        self.registry_menu_clicked()

    # Ativa página 'registrar' e entra no modo inserção
    def registry_menu_clicked(self):
        self.ID = -1
        self.clear_registry()

    # Ativa página 'pesquisar'
    def search_menu_clicked(self):
        self.mp_main.setCurrentIndex(1)
        self.statusBar.clearMessage()
        self.txt_nfe_search.setFocus()

    # Ativa página 'exportar'
    def export_menu_clicked(self):
        self.mp_main.setCurrentIndex(2)
        self.statusBar.clearMessage()

    # Cria ou edita registro no banco de dados
    def save_registry(self):
        fields = [
            self.txt_nfe,
            self.txt_date,
            self.cb_supplier,
            self.txt_value
        ]

        # Verifica se há campos em branco
        empty_fields = get_empty_fields(fields)

        if len(empty_fields) > 0:
            QMessageBox.warning(self, 'ATENÇÃO', 'Preencha os campos obrigatórios!')
            empty_fields[0].setFocus()
            return

        date = parse_date(fields[1].text(), '%d/%m/%Y', '%Y-%m-%d')

        # Verifica se é uma data válida
        if not date:
            QMessageBox.warning(self, 'ATENÇÃO', 'Data inválida!')
            self.txt_date.setFocus()
            return

        # Cria dicionário com dados
        fields = {
            'nfe': fields[0].text(),
            'date': date,
            'supplier': fields[2].currentText().upper(),
            'value': from_currency_to_float(fields[3].text())
        }

        # Caso ID seja -1 então estamos em modo de inserção
        if self.ID == -1:

            # Verifica se já existe um registro com a mesma nfe e fornecedor no banco de dados
            query = read(
                table='history',
                fields=['count(*)'],
                where={
                    'clause': 'WHERE nfe LIKE ? AND supplier LIKE ?',
                    'values': [fields['nfe'], fields['supplier']]
                }
            )

            query.first()

            if query.value(0) > 0:
                QMessageBox.warning(self, 'ATENÇÃO', 'Essa nota já foi registrada com esse fornecedor!')
                return

            message = 'Deseja inserir esse registro no banco de dados?'
        else:
            message = 'Deseja editar esse registro no banco de dados?'

        # Faz pergunta de seguraça ao usuário, caso não confirme aborta ação
        answer = self.message.show_message(
            'ATENÇÃO',
            message,
            QMessageBox.Icon.Warning,
            default_button=self.yes
        )

        if answer == self.no:
            return

        # Caso fornecedor não se encontre no banco de dados, o adiciona
        supplier = self.cb_supplier.currentText().upper()

        if self.cb_supplier.findText(supplier) == -1:
            create(table='suppliers', fields={'supplier': supplier})
            self.load_suppliers()

        # Caso esteja em modo de inserção
        if self.ID == -1:
            create(table='history', fields=fields)
            message = 'Registro inserido com sucesso.'
        # Do contrário se trata de modo de edição
        else:
            update(table='history', fields=fields, id_record=self.ID)
            message = 'Registro alterado com sucesso.'

        # Prepara para novo registro e avisa usuário
        QMessageBox.information(self, 'AVISO', message)
        self.registry_menu_clicked()

        # Faz nova pesquisa na página 'pesquisar'
        self.search()

    # Limpa campos da página registro
    def clear_registry(self):
        self.txt_nfe.clear()
        self.txt_date.clear()
        self.cb_supplier.lineEdit().setText('')
        self.txt_value.clear()

        self.txt_nfe.setFocus()

    # Deleta registro
    def delete_registry(self):
        answer = self.message.show_message(
            'ATENÇÃO',
            'Deseja deletar esse registro no banco de dados?',
            QMessageBox.Icon.Warning,
            default_button=self.no
        )

        if answer == self.no:
            return

        # Deleta registro
        delete(table='history', id_record=self.ID)

        # Prepara para novo registro e avisa usuário
        QMessageBox.information(self, 'AVISO', 'Registro deletado com sucesso.')
        self.registry_menu_clicked()

        # Faz nova pesquisa na página 'pesquisar'
        self.search()

    # Limpa campos da página de pesquisa
    def clear_search(self):
        self.txt_nfe_search.clear()
        self.txt_supplier_search.clear()
        self.txt_start_date.clear()
        self.txt_end_date.clear()

        self.txt_nfe_search.setFocus()

    # Pesquisa dados no banco de dados e insere na QTableView
    def search(self):
        nfe = self.txt_nfe_search.text()
        supplier = self.txt_supplier_search.text()
        start_date = parse_date(self.txt_start_date.text(), '%d/%m/%Y', '%Y-%m-%d', on_fail=DateMinMax.MIN)
        end_date = parse_date(self.txt_end_date.text(), '%d/%m/%Y', '%Y-%m-%d', on_fail=DateMinMax.MAX)

        try:
            # Realiza consulta
            query = read(
                table='history',
                fields=['id', 'nfe', 'date', 'supplier', 'value'],
                where={
                    'clause': "WHERE nfe LIKE '%' || ? ||  '%' AND supplier LIKE '%' || ? || '%' AND date >= ? AND "
                              "date <= ? ORDER BY date",
                    'values': [nfe, supplier, start_date, end_date]
                }
            )
            # Seta resultado da query ao model
            self.model.setQuery(query)

            # Seta headers do model
            self.model.setHeaderData(1, Qt.Orientation.Horizontal, 'NFE')
            self.model.setHeaderData(2, Qt.Orientation.Horizontal, 'DATA')
            self.model.setHeaderData(3, Qt.Orientation.Horizontal, 'FORNECEDOR')
            self.model.setHeaderData(4, Qt.Orientation.Horizontal, 'VALOR')

            # Esconde a coluna de ID e redimensiona colunas
            self.table_search.setColumnHidden(0, True)
            self.table_search.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        except QueryError as e:
            QMessageBox.critical(
                self,
                'CRÍTICO',
                f'Não foi possível realizar a consulta, verifique a query.\n\n{e.query}'
            )

    # Exporta relatório em pdf
    def export_pdf(self):
        answer = self.message.show_message(
            'ATENÇÃO',
            'Deseja exportar o relatório em pdf?',
            QMessageBox.Icon.Question,
            default_button=self.yes
        )

        if answer == self.no:
            return

        # Seta nome inicial e abre caixa de diálogo para usuário selecionar local para salvar
        inicial_name = f'RELATÓRIO DE NOTAS {self.cb_month.currentText()} DE {self.cb_year.currentText()}'
        path = QFileDialog.getSaveFileName(self.centralwidget, 'Salvar em PDF.', inicial_name, 'pdf (*.pdf)')[0]

        # Configura layout
        layout = QPageLayout(
            QPageSize(QPageSize.PageSizeId.A4),
            QPageLayout.Orientation.Portrait,
            QMarginsF(0, 20, 0, 20)
        )

        # Caso usuário selecione um local, salva em pdf e informa usuário
        if path:
            self.web_view.printToPdf(path, layout)
            QMessageBox.information(self, 'AVISO', 'Relatório exportado!')

    # Imprime relatório
    def print_report(self):
        answer = self.message.show_message(
            'ATENÇÃO',
            'Deseja imprimir o relátorio?',
            QMessageBox.Icon.Question,
            default_button=self.yes
        )

        if answer == self.no:
            return

        # Imprime relatório e avisa usuário
        printer = QPrinter()
        printer.setPageMargins(QMarginsF(0, 20, 0, 20))
        self.web_view.print(printer)

        QMessageBox.information(self, 'AVISO', 'Relatório impresso!')

    # Traz dados da QTableView para a página de registro
    def history_record_selected(self, index: QModelIndex | int):
        # Pega linha clicada
        row = index.row() if isinstance(index, QModelIndex) else index

        # Obtém dados
        id_record = self.model.index(row, 0).data()
        nfe = self.model.index(row, 1).data()
        date = self.model.index(row, 2).data()
        supplier = self.model.index(row, 3).data()
        value = self.model.index(row, 4).data()

        # Seta dados nos campos
        self.txt_nfe.setText(str(nfe))
        self.txt_date.setText(date)
        self.cb_supplier.lineEdit().setText(supplier)
        self.txt_value.setText(value)

        # Entra em modo de edição
        self.ID = id_record

    # Carrega fornecedores
    def load_suppliers(self):
        query = read(
            table='suppliers',
            fields=['supplier'],
            where={
                'clause': 'ORDER BY supplier',
                'values': []
            }
        )

        data = []

        while query.next():
            data.append(query.value(0))

        self.cb_supplier.clear()
        self.cb_supplier.addItems(data)

    # Cria relatório
    def create_report(self):
        month = self.cb_month.currentText()
        year = self.cb_year.currentText()

        # Pega o range do mês com base no ano e no mês atual
        start_date, end_date = parse_month(self.cb_month.currentIndex() + 1, int(year))

        rows = []
        total = 0

        # Realiza query para pegar dados no range
        queue = read(
            'history',
            fields=['nfe', 'date', 'supplier', 'value'],
            where={
                'clause': "WHERE date >= ? AND date <= ? ORDER BY date",
                'values': [start_date, end_date]
            }
        )

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

        # Cria dicionário com dados
        data = {
            'rows': rows,
            'total': from_float_to_currency(total),
            'year': year,
            'month': month
        }

        # Recebe template formatado e insere na web_view
        html = create_html(data)
        self.web_view.setHtml(html)


# Usado para auxiliar na depuração
def exception_hook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)
    sys.exit(1)


# Inicia o aplicativo
if __name__ == "__main__":
    try:
        # noinspection PyUnresolvedReferences
        from ctypes import windll

        myappid = 'kamua.nfe_report.1.0.0'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        pass

    sys.excepthook = exception_hook

    qt = QApplication(sys.argv)
    qt.setStyle('Fusion')
    qt.setWindowIcon(QIcon(os.path.join(BASEDIR, 'assets/task-64.png')))

    try:
        # noinspection PyUnresolvedReferences
        import pyi_splash

        pyi_splash.close()
    except ModuleNotFoundError:
        pass

    app = App()
    app.show()

    sys.exit(qt.exec())
