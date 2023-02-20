import sys
import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QHeaderView, QLabel
from PyQt6.QtCore import Qt, QModelIndex, QMarginsF, QRegularExpression
from PyQt6.QtGui import QPageLayout, QIcon, QPageSize, QRegularExpressionValidator, QCloseEvent
from PyQt6.QtPrintSupport import QPrinter

from ui.MainWindow import Ui_MainWindow
from utils import *
from services import *


# Janela principal
class App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Instancia variáveis
        self._ID: int | None = None
        self.model: TableModel | None = None
        self.status_message: QLabel | None = None

        # Abre conexão com o banco de dados
        self.database = DatabaseConnection()
        self.database.connect()

        # Inicialização
        self.init_ui()

        # Realiza o backup
        do_backup(self.database)

        # Define a primeira página ao abrir o progrma
        self.registry_menu_clicked()

    # Fecha conexão com banco de dados ao fechar o aplicativo
    def closeEvent(self, a0: QCloseEvent) -> None:
        self.database.disconnect()
        a0.accept()

    # ID encapsulado
    @property
    def ID(self):
        return self._ID

    # Setter para automatizar ações ao alterar ID
    @ID.setter
    def ID(self, value):
        flag = bool(value + 1)
        message = f'Modo: Editar | ID: {value}' if flag else f'Modo: Registrar'

        self.status_message.setText(message)
        self.bt_delete.setDisabled(not flag)
        self.mp_main.setCurrentIndex(0)
        self.txt_nfe.setFocus()

        self._ID = value

    # Inicia elementos
    def init_ui(self):
        # Conecta botões do menu nas páginas do stacked widget
        self.bt_register_menu.clicked.connect(lambda: self.registry_menu_clicked())
        self.bt_search_menu.clicked.connect(lambda: self.search_menu_clicked())
        self.bt_export_menu.clicked.connect(lambda: self.export_menu_clicked())

        self.status_message = QLabel(self)
        self.status_message.setStyleSheet("margin: 0px 0px 5px 5px;")
        self.statusBar.addWidget(self.status_message)

        # Define icon, título e tamanho da janela
        self.setWindowIcon(QIcon(os.path.join(BASEDIR, 'assets/task-64.png')))
        self.setWindowTitle('Relatório de Notas')
        self.setFixedSize(785, 560)

        # Define atalho ao clicar na tecla ENTER na tela de pesquisa
        self.bt_search.setShortcut('Return')

        # Configura web view
        self.web_view.setZoomFactor(0.8)
        self.web_view.setHtml('')

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

        # Seta model para list view e faz pesquisa
        self.model = TableModel()
        self.table_search.setModel(self.model)

        # Seta botões do menu
        self.action_config.triggered.connect(lambda: ConfigurationDialog(self, self.database).show())
        self.action_suppliers.triggered.connect(lambda: SupplierDialog(self, self.database).show())
        self.action_years.triggered.connect(lambda: YearDialog(self, self.database).show())
        self.action_import_backup.triggered.connect(lambda: ImportBackupDialog(self, self.database).show())

        # Remove valor inicial do ComboBox e alinha ao centro
        self.cb_supplier.setCurrentIndex(-1)
        self.cb_supplier.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Define slots para os botões da página 'Registrar'
        self.bt_save.clicked.connect(self.save_registry)
        self.bt_clear.clicked.connect(self.clear_registry)
        self.bt_delete.clicked.connect(self.delete_registry)
        self.bt_calendar_date.clicked.connect(lambda: CalendarDialog(self, self.txt_date, 'Data').show())

        # Define slots para os botões da página 'Pesquisar'
        self.bt_clear_search.clicked.connect(self.clear_search)
        self.bt_search.clicked.connect(self.search)
        self.bt_calendar_start_date.clicked.connect(
            lambda: CalendarDialog(self, self.txt_start_date, 'Data Inicial').show())
        self.bt_calendar_end_date.clicked.connect(lambda: CalendarDialog(self, self.txt_end_date, 'Data Final').show())

        # Define slots para o evento de double click na table view
        self.table_search.doubleClicked.connect(self.history_record_selected)
        self.table_search.verticalHeader().sectionDoubleClicked.connect(self.history_record_selected)

        # Define slots para os botões da página 'Exportar'
        self.bt_pdf.clicked.connect(self.export_pdf)
        self.bt_print.clicked.connect(self.print_report)
        self.cb_month.currentIndexChanged.connect(self.create_report)
        self.cb_year.currentIndexChanged.connect(self.create_report)

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

    def start_app(self):
        # Verifica conexão após iniciar janela principal
        if self.database.connection_state == DatabaseConnection.State.DATABASE_NOT_FOUND:
            Message.critical(
                self,
                'CRÍTICO',
                'Erro ao acessar banco de dados!\n'
                'Se seu banco de dados estiver na rede verifique se há conexão com a internet.'
            )
        elif self.database.connection_state == DatabaseConnection.State.NO_DATABASE:
            Message.warning(self, 'ATENÇÃO', 'Insira um banco de dados para usar o programa.')
            self.action_config.trigger()

        # Configura dados
        self.setup_data()

        # Seta ano e mês atual
        current_month, current_year = get_current_month_year()
        self.cb_month.setCurrentIndex(current_month - 1)
        self.cb_year.setCurrentText(str(current_year))

    def setup_data(self):
        # Verifica conexão
        connected = self.database.connection_state == DatabaseConnection.State.CONNECTED

        # Se não houver conexão desabiilita funções do aplicativo
        self.action_years.setDisabled(not connected)
        self.action_suppliers.setDisabled(not connected)
        self.mp_main.setDisabled(not connected)

        if connected:
            # Carrega dados para dentro do app
            self.load_years()
            self.load_suppliers()
            self.create_report()
            self.search()

    # Ativa página 'registrar' e entra no modo inserção
    def registry_menu_clicked(self):
        self.ID = -1
        self.clear_registry()

    # Ativa página 'pesquisar'
    def search_menu_clicked(self):
        self.mp_main.setCurrentIndex(1)
        self.status_message.setText('')
        self.txt_nfe_search.setFocus()

    # Ativa página 'exportar'
    def export_menu_clicked(self):
        self.mp_main.setCurrentIndex(2)
        self.status_message.setText('')

    # Cria ou edita registro no banco de dados
    @check_connection
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
            Message.warning(self, 'ATENÇÃO', 'Preencha os campos obrigatórios!')
            empty_fields[0].setFocus()
            return

        date = parse_date(fields[1].text(), '%d/%m/%Y', '%Y-%m-%d')

        # Verifica se é uma data válida
        if not date:
            Message.warning(self, 'ATENÇÃO', 'Data inválida!')
            self.txt_date.setFocus()
            return

        # Cria dicionário com dados
        fields = {
            'nfe': fields[0].text(),
            'date': date,
            'supplier': fields[2].currentText().upper(),
            'value': from_currency_to_float(fields[3].text())
        }

        message = 'Deseja editar esse registro no banco de dados?'

        # Caso ID seja -1 então estamos em modo de inserção
        if self.ID == -1:
            # Verifica se já existe um registro com a mesma nfe e fornecedor no banco de dados
            query = self.database.read(
                table='history',
                fields=['count(*)'],
                where={
                    'clause': 'WHERE nfe LIKE ? AND supplier LIKE ?',
                    'values': [fields['nfe'], fields['supplier']]
                }
            )

            query.first()

            if query.value(0) > 0:
                Message.warning(self, 'ATENÇÃO', 'Essa nota já foi registrada com esse fornecedor!')
                return

            message = message.replace('editar', 'inserir')

        # Faz pergunta de segurança ao usuário, caso não confirme aborta ação
        if Message.warning_question(self, message, Message.YES) == Message.NO:
            return

        # Caso fornecedor não se encontre no banco de dados, o adiciona
        supplier = self.cb_supplier.currentText().upper()

        if self.cb_supplier.findText(supplier) == -1:
            self.database.create(table='suppliers', fields={'supplier': supplier})
            self.load_suppliers()

        try:
            # Caso esteja em modo de inserção
            if self.ID == -1:
                self.database.create(table='history', fields=fields)
                message = 'Registro inserido com sucesso.'
            # Do contrário se trata de modo de edição
            else:
                self.database.update(table='history', fields=fields, id_record=self.ID)
                message = 'Registro alterado com sucesso.'

            # Prepara para novo registro e avisa usuário
            Message.information(self, 'AVISO', message)
            self.registry_menu_clicked()

            # Faz nova pesquisa na página 'pesquisar'
            self.search()
        except QueryError:
            Message.critical(self, 'CRÍTICO', 'Algo deu errado durante a operação!')

    # Limpa campos da página registro
    @check_connection
    def clear_registry(self):
        self.txt_nfe.clear()
        self.txt_date.clear()
        self.cb_supplier.lineEdit().setText('')
        self.txt_value.clear()

        self.txt_nfe.setFocus()

    # Deleta registro
    @check_connection
    def delete_registry(self):
        if Message.warning_question(self, 'Deseja deletar esse registro no banco de dados?') == Message.NO:
            return

        # Deleta registro
        try:
            self.database.delete(table='history', clause=f'id LIKE {self.ID}')

            # Prepara para novo registro e avisa usuário
            Message.information(self, 'AVISO', 'Registro deletado com sucesso.')
            self.registry_menu_clicked()

            # Faz nova pesquisa na página 'pesquisar'
            self.search()
        except QueryError:
            Message.critical(self, 'CRÍTICO', 'Algo deu errado durante a operação!')

    # Limpa campos da página de pesquisa
    @check_connection
    def clear_search(self):
        self.txt_nfe_search.clear()
        self.txt_supplier_search.clear()
        self.txt_start_date.clear()
        self.txt_end_date.clear()

        self.txt_nfe_search.setFocus()

    # Pesquisa dados no banco de dados e insere na QTableView
    @check_connection
    def search(self):
        nfe = self.txt_nfe_search.text()
        supplier = self.txt_supplier_search.text()
        start_date = parse_date(self.txt_start_date.text(), '%d/%m/%Y', '%Y-%m-%d', on_fail=DateMinMax.MIN)
        end_date = parse_date(self.txt_end_date.text(), '%d/%m/%Y', '%Y-%m-%d', on_fail=DateMinMax.MAX)

        try:
            # Realiza consulta
            query = self.database.read(
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
            Message.critical(
                self,
                'CRÍTICO',
                f'Não foi possível realizar a consulta, verifique a query.\n\n{e.query}'
            )

    # Exporta relatório em pdf
    def export_pdf(self):
        if Message.warning_question(self, 'Deseja exportar o relatório em pdf?', Message.YES) == Message.NO:
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
            Message.information(self, 'AVISO', 'Relatório exportado!')

    # Imprime relatório
    def print_report(self):
        if Message.warning_question(self, 'Deseja imprimir o relátorio?', Message.YES) == Message.NO:
            return

        # Imprime relatório e avisa usuário
        printer = QPrinter()
        printer.setPageMargins(QMarginsF(0, 20, 0, 20))
        self.web_view.print(printer)

        Message.information(self, 'AVISO', 'Relatório impresso!')

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

    # Carrega anos armazenados
    @check_connection
    def load_years(self):
        years = get_years(self.database)

        self.cb_year.clear()
        self.cb_year.addItems(years)

    # Carrega fornecedores
    @check_connection
    def load_suppliers(self):
        query = self.database.read(
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
        self.cb_supplier.setCurrentIndex(-1)

    # Cria relatório
    @check_connection
    def create_report(self):
        month = self.cb_month.currentText()
        year = self.cb_year.currentText()

        # Pega o range do mês com base no ano e no mês atual
        start_date, end_date = parse_month(self.cb_month.currentIndex() + 1, int(year))

        rows = []
        total = 0

        # Realiza query para pegar dados no range do mês
        query = self.database.read(
            table='history',
            fields=['nfe', 'date', 'supplier', 'value'],
            where={
                'clause': "WHERE date >= ? AND date <= ? ORDER BY date",
                'values': [start_date, end_date]
            }
        )

        while query.next():
            nfe = query.value(0)
            date = query.value(1)
            supplier = query.value(2)
            value = query.value(3)

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
    # Altera id do aplicativo para evitar bugs com o ícone na barra de tarefas
    try:
        # noinspection PyUnresolvedReferences
        from ctypes import windll

        myappid = 'kamua.nfe_report.1.0.0'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        pass

    # Vincula hook personalizado para receber logs durante desenvolvimento
    sys.excepthook = exception_hook

    qt = QApplication(sys.argv)
    qt.setStyle('Fusion')
    qt.setWindowIcon(QIcon(os.path.join(BASEDIR, 'assets/task-64.png')))

    # Desativa splash do pyinstaller quando a aplicação carregar
    try:
        # noinspection PyUnresolvedReferences
        import pyi_splash

        pyi_splash.close()
    except ModuleNotFoundError:
        pass

    app = App()
    app.show()
    app.start_app()

    sys.exit(qt.exec())
