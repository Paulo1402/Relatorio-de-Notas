"""
Ponto de entrada do programa.

Esse arquivo é compilado usando a lib PyInstaller para gerar um executável para distribuição.
"""
import sys
import warnings
import locale

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QHeaderView, QLabel, QProgressBar
from PySide6.QtCore import Qt, QModelIndex, QMarginsF, QRegularExpression, Slot
from PySide6.QtGui import QPageLayout, QIcon, QPageSize, QRegularExpressionValidator, QCloseEvent, QAction
from PySide6.QtPrintSupport import QPrinter, QPrintDialog

from ui.MainWindow import Ui_MainWindow
from services import *
from utils import *
from dialog import *

# todo FrontEnd
#   Adicionar dark / light mode
#   Adicionar efeitos CSS
#   Adicionar fixup no campo de data
#   Adicionar auto format no campo de valor

# todo BackEnd
#   Usar PDFtoPrinter.exe para imprimir relatório, é possível exportar em PDF na pasta temp para depois imprimir

# todo Refactoring
#   Restruturar projeto para o novo formato (Se basear no projeto Controle de Estoque)
#   Atualizar bindings para usar PySide6

# todo Testes

# todo Bugs

"""
    possible solution is to use PDFtoPrinter.exe
    http://www.columbia.edu/~em36/pdftoprinter.html?fbclid=IwAR1kRJ8oWyduJ_HreuBMdQEIUlUZWYCJFzN8yVGUITmXXd6ei74kVwusSDE
    
    import subprocess

    def command_print(event = None):
        command = "{} {}".format('PDFtoPrinter.exe','report.pdf')
        subprocess.call(command,shell=True)
    
    command_print()
"""


# Janela principal
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Instancia variáveis
        self.model: TableModel | None = None
        self.printer: QPrinter | None = None

        self._ID = -1

        # Abre conexão com o banco de dados
        self.database = DatabaseConnection()
        self.database.connect()

        # Cria widgets de backup
        self.backup_bar = QProgressBar()
        self.backup_label = QLabel('Realizando backup...')
        self.backup_worker: DoBackupWorker | None = None

        # Inicialização
        self.init_ui()

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value: int):
        """Setter para automatizar ações ao alterar ID."""
        self._ID = value
        flag = bool(value + 1)

        self.bt_delete.setDisabled(not flag)
        self.mp_main.setCurrentIndex(0)
        self.txt_nfe.setFocus()

        self.handle_status_message(value)

    def closeEvent(self, event: QCloseEvent):
        """Disparado quando a janela é fechada"""
        if Message.warning_question(self, 'Deseja fechar o aplicativo?') == Message.NO:
            event.ignore()
            return

        self.database.disconnect()
        event.accept()

    def show(self):
        """Inicia janela principal."""
        super().show()

        # Verifica conexão após iniciar janela principal
        if self.database.connection_state == DatabaseConnection.State.DATABASE_NOT_FOUND:
            Message.critical(
                self,
                'CRÍTICO',
                'Erro ao acessar banco de dados!\n'
                'Se seu banco de dados estiver na rede verifique se há conexão com o computador servidor.'
            )
        elif self.database.connection_state == DatabaseConnection.State.NO_DATABASE:
            Message.warning(self, 'ATENÇÃO', 'Insira um banco de dados para usar o programa.')
            self.action_config.trigger()
        else:
            # Cria worker para fazer o backup
            self.backup_worker = DoBackupWorker(self.database)
            self.backup_worker.progress.connect(self.backup_progress)
            self.backup_worker.finished.connect(self.backup_finished)

            # Inicia worker
            self.backup_worker.start()

            # Retorna ano e mês atual
            current_month, current_year = get_current_month_year()

            # Bloqueia eventos para inserir o mês atual
            self.cb_month.blockSignals(True)
            self.cb_month.setCurrentIndex(current_month - 1)
            self.cb_month.blockSignals(False)

            # Insere ano atual pelo índice
            index = self.cb_year.findText(str(current_year))
            self.cb_year.setCurrentIndex(index)

        # Configura dados
        self.setup_data()

    def init_ui(self):
        """Realiza conexões de signals e slots"""
        self.setWindowTitle(APP_NAME.upper())
        self.setFixedSize(850, 560)

        # Conecta botões do menu principal
        self.bt_register_menu.clicked.connect(lambda: self.registry_menu_clicked())
        self.bt_search_menu.clicked.connect(lambda: self.search_menu_clicked())
        self.bt_export_menu.clicked.connect(lambda: self.export_menu_clicked())

        # Seta botões do menu de tarefas
        self.action_config.triggered.connect(lambda: DatabaseConfigDialog(self, self.database).show())
        self.action_import_backup.triggered.connect(lambda: ImportBackupDialog(self, self.database).show())
        self.action_suppliers.triggered.connect(lambda: SupplierDialog(self, self.database).show())
        self.action_years.triggered.connect(lambda: YearDialog(self, self.database).show())
        self.action_light_theme.triggered.connect(lambda: self.handle_theme('light'))
        self.action_dark_theme.triggered.connect(lambda: self.handle_theme('dark'))

        # É necessário suprimir esse evento para não remover a mensagem de edição da status bar,
        # quando o menu bar disparar o evento de hover
        self.menubar.installEventFilter(StatusTipEventFilter(self))

        # Adiciona widgets a status bar
        self.statusBar().addPermanentWidget(self.backup_label)
        self.statusBar().addPermanentWidget(self.backup_bar)
        self.backup_label.setVisible(False)
        self.backup_bar.setVisible(False)

        # Página Registro
        self.cb_supplier.setCurrentIndex(-1)
        self.cb_supplier.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.bt_save.clicked.connect(self.save_registry)
        self.bt_clear.clicked.connect(self.clear_registry)
        self.bt_delete.clicked.connect(self.delete_registry)

        # Página Pesquisa
        action = QAction(self)
        action.setShortcuts(['Return', 'Enter'])
        self.bt_search.addAction(action)

        self.table_search.setModel(TableModel())
        self.table_search.doubleClicked.connect(self.edit_registry)
        self.table_search.verticalHeader().sectionDoubleClicked.connect(self.edit_registry)

        self.bt_clear_search.clicked.connect(self.clear_search)
        self.bt_search.clicked.connect(self.search)

        # Página Exportar
        self.web_view.setZoomFactor(0.8)
        self.web_view.setHtml('')

        months = get_months_name()
        self.cb_month.addItems(months)

        self.bt_pdf.clicked.connect(self.export_pdf)
        self.bt_print.clicked.connect(self.print_report)
        self.cb_month.currentIndexChanged.connect(self.create_report)
        self.cb_year.currentIndexChanged.connect(self.create_report)

        # Seta validadores
        validator = DateValidator()
        self.cb_date.setValidator(validator)
        self.cb_start_date.setValidator(validator)
        self.cb_end_date.setValidator(validator)

        validator = QRegularExpressionValidator(QRegularExpression(r'\d+(,\d+)?'))
        self.txt_value.setValidator(validator)

        validator = QRegularExpressionValidator(QRegularExpression(r'[1-9]\d*'))
        self.txt_nfe_search.setValidator(validator)
        self.txt_nfe.setValidator(validator)

    def setup_data(self):
        # Verifica conexão
        connected = self.database.connection_state == DatabaseConnection.State.CONNECTED

        # Se não houver conexão desabilita funções do aplicativo
        self.action_years.setDisabled(not connected)
        self.action_suppliers.setDisabled(not connected)
        self.action_import_backup.setDisabled(not connected)
        self.mp_main.setDisabled(not connected)

        if connected:
            # Carrega dados para dentro do app
            self.load_years()
            self.load_suppliers()
            self.create_report()
            self.search()

    @Slot()
    def backup_progress(self, progress: int):
        """Atualiza widgets de backup"""
        if not self.backup_bar.isVisible():
            self.backup_bar.setVisible(True)
            self.backup_label.setVisible(True)

        self.backup_bar.setValue(progress)

    @Slot()
    def backup_finished(self):
        """Limpa worker e esconde widgets"""
        self.backup_label.setVisible(False)
        self.backup_bar.setVisible(False)

        self.backup_worker = None

    @Slot()
    def handle_status_message(self, value: int):
        """Manipula status bar."""
        if value != -1:
            message = f'EDITANDO REGISTRO: {value}'
            self.statusBar().showMessage(message)
        else:
            self.statusBar().clearMessage()

    # Ativa página 'registrar' e entra no modo inserção
    def registry_menu_clicked(self):
        self.ID = -1
        self.clear_registry()
        self.handle_status_message(self.ID)

    # Ativa página 'pesquisar'
    def search_menu_clicked(self):
        self.mp_main.setCurrentIndex(1)
        self.txt_nfe_search.setFocus()
        self.handle_status_message(self.ID)

    # Ativa página 'exportar'
    def export_menu_clicked(self):
        self.mp_main.setCurrentIndex(2)
        self.handle_status_message(self.ID)

    # Cria ou edita registro no banco de dados
    @check_connection
    def save_registry(self):
        fields = [
            self.txt_nfe,
            self.cb_date,
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
            self.cb_date.setFocus()
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
                clause='WHERE nfe LIKE ? AND supplier LIKE ?',
                values=[fields['nfe'], fields['supplier']]
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
                self.database.update(table='history', fields=fields, clause=f'WHERE id LIKE {self.ID}')
                message = 'Registro alterado com sucesso.'

            # Prepara para novo registro e avisa usuário
            Message.information(self, 'AVISO', message)
            self.registry_menu_clicked()

            # Faz nova pesquisa na página 'pesquisar'
            self.search()
        except QueryError:
            Message.critical(self, 'CRÍTICO', 'Algo deu errado durante a operação!')

    # Limpa campos da página registro
    def clear_registry(self):
        self.txt_nfe.clear()
        self.cb_date.clear()
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
            self.database.delete(table='history', clause=f'WHERE id LIKE {self.ID}')

            # Prepara para novo registro e avisa usuário
            Message.information(self, 'AVISO', 'Registro deletado com sucesso.')
            self.registry_menu_clicked()

            # Faz nova pesquisa na página 'pesquisar'
            self.search()
        except QueryError:
            Message.critical(self, 'CRÍTICO', 'Algo deu errado durante a operação!')

    # Limpa campos da página de pesquisa
    def clear_search(self):
        self.txt_nfe_search.clear()
        self.txt_supplier_search.clear()
        self.cb_start_date.clear()
        self.cb_end_date.clear()

        self.txt_nfe_search.setFocus()

    # Pesquisa dados no banco de dados e insere na QTableView
    @check_connection
    def search(self):
        nfe = self.txt_nfe_search.text()
        supplier = self.txt_supplier_search.text()
        start_date = parse_date(self.cb_start_date.currentText(), '%d/%m/%Y', '%Y-%m-%d', on_fail=DateMinMax.MIN)
        end_date = parse_date(self.cb_end_date.currentText(), '%d/%m/%Y', '%Y-%m-%d', on_fail=DateMinMax.MAX)

        try:
            # Realiza consulta
            query = self.database.read(
                table='history',
                fields=['id', 'nfe', 'date', 'supplier', 'value'],
                clause="WHERE nfe LIKE '%' || ? ||  '%' AND supplier LIKE '%' || ? || '%'" \
                       "AND date >= ? AND date <= ? ORDER BY date",
                values=[nfe, supplier, start_date, end_date]
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

        # Caso usuário selecione um local, salva em pdf e informa usuário
        if path:
            # Configura layout
            layout = QPageLayout(
                QPageSize(QPageSize.PageSizeId.A4),
                QPageLayout.Orientation.Portrait,
                QMarginsF(0, 20, 0, 20)
            )

            self.web_view.printToPdf(path, layout)
            Message.information(self, 'AVISO', 'Relatório exportado!')

    # Imprime relatório
    def print_report(self):
        if Message.warning_question(self, 'Deseja imprimir o relátorio?', Message.YES) == Message.NO:
            return

        self.printer = QPrinter()
        dialog = QPrintDialog(self.printer, self)

        if dialog.exec() == QPrintDialog.DialogCode.Rejected:
            return

        # Configura layout
        # layout = QPageLayout(
        #     QPageSize(QPageSize.PageSizeId.A4),
        #     QPageLayout.Orientation.Portrait,
        #     QMarginsF(0, 50, 0, 50)
        # )

        # self.printer.setPageLayout(layout)

        # self.printer.setResolution(QPrinter.PrinterMode.HighResolution)

        self.web_view.printFinished.connect(self.finished_printing)
        self.web_view.print(self.printer)

    def finished_printing(self, success: bool):
        if success:
            Message.information(self, 'AVISO', 'Relatório impresso!')
        else:
            Message.critical(self, 'CRÍTICO', 'Algo deu errado durante a impressão, se a impressora está na rede '
                                              'verifique a conexão, por favor.')

    # Traz dados da QTableView para a página de registro
    def edit_registry(self, index: QModelIndex | int):
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
        self.cb_date.setCurrentText(date)
        self.cb_supplier.lineEdit().setText(supplier)
        self.txt_value.setText(value)

        # Entra em modo de edição
        self.ID = id_record

    # Carrega anos armazenados
    @check_connection
    def load_years(self):
        self.cb_year.blockSignals(True)

        years = self.database.get_years(self.database)
        self.cb_year.clear()
        self.cb_year.addItems(years)

        self.cb_year.blockSignals(False)

    # Carrega fornecedores
    @check_connection
    def load_suppliers(self):
        query = self.database.read(
            table='suppliers',
            fields=['supplier'],
            clause='ORDER BY supplier'
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
        start_date, end_date = get_range_month(self.cb_month.currentIndex() + 1, int(year))

        rows = []
        total = 0

        # Realiza query para pegar dados no range do mês
        query = self.database.read(
            table='history',
            fields=['nfe', 'date', 'supplier', 'value'],
            clause='WHERE date >= ? AND date <= ? ORDER BY date',
            values=[start_date, end_date]
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


def exception_hook(*args, **kwargs):
    """Custom hook para receber exceptions vindas do C++(QT) durante desenvolvimento"""
    sys.__excepthook__(*args, **kwargs)
    sys.exit(1)


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
    sys.excepthook = exception_hook

    if not DEBUG:
        warnings.filterwarnings('ignore', category=DeprecationWarning)

    # Altera id do aplicativo para evitar bugs com o ícone na barra de tarefas
    try:
        # noinspection PyUnresolvedReferences
        from ctypes import windll

        myappid = 'kamua.relatorio_de_notas.1.0.0'
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except ImportError:
        pass

    # noinspection PyBroadException
    try:
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon(u":/icons/assets/task-64.png"))

        window = MainWindow()
        window.setStyleSheet('')
        window.show()

        tb = app.exec()

        if tb != 0:
            Logger().error(tb)

        sys.exit(tb)
    except Exception:
        Logger().exception('')
