"""
Ponto de entrada do programa.

Esse arquivo é compilado usando a lib PyInstaller para gerar um executável para distribuição.
"""
import os
import sys
import warnings
import locale

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QHeaderView, QLabel, QProgressBar
from PySide6.QtCore import Qt, QModelIndex, QMarginsF, QRegularExpression, Slot, QTimer
from PySide6.QtGui import QPageLayout, QIcon, QPageSize, QRegularExpressionValidator, QCloseEvent, QAction

from ui.MainWindow import Ui_MainWindow
from services import *
from utils import *
from dialog import *


class MainWindow(QMainWindow, Ui_MainWindow):
    """Janela principal do aplicativo."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.timer: QTimer | None = None
        self.temp_files: list = []
        self._ID: int = -1
        self.current_year: str | None = None

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
        self.txt_nfe.setFocus()

        self.handle_status_message(value)

    def closeEvent(self, event: QCloseEvent):
        """Disparado quando a janela é fechada"""
        if Message.warning_question(self, 'Deseja fechar o aplicativo?') == Message.NO:
            event.ignore()
            return

        # Remove arquivos temporários gerados
        for file in self.temp_files:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass

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
            self.current_year = str(current_year)

            # Bloqueia eventos para inserir o mês atual
            self.cb_month.blockSignals(True)
            self.cb_month.setCurrentIndex(current_month - 1)
            self.cb_month.blockSignals(False)

        # Configura dados
        self.setup_data()

    def init_ui(self):
        """Realiza conexões de signals e slots"""
        self.setWindowTitle(APP_NAME.upper())

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
        self.statusBar.addPermanentWidget(self.backup_label)
        self.statusBar.addPermanentWidget(self.backup_bar)
        self.backup_label.setVisible(False)
        self.backup_bar.setVisible(False)

        # Página Registro
        self.cb_supplier.setCurrentIndex(-1)
        self.cb_supplier.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cb_date.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.bt_save.clicked.connect(self.save_registry)
        self.bt_new.clicked.connect(self.new_registry)
        self.bt_delete.clicked.connect(self.delete_registry)

        # Página Pesquisa
        action = QAction(self)
        action.setShortcuts(['Return', 'Enter'])
        action.triggered.connect(lambda: self.bt_search.animateClick())
        self.addAction(action)

        self.table_search.setModel(TableModel(date_fields=[2], currency_fields=[4]))
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
        self.cb_month.currentIndexChanged.connect(lambda: self.create_report())
        self.cb_year.currentIndexChanged.connect(lambda: self.create_report())

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

        # Carrega tema configurado
        config = get_config(ConfigSection.APP)
        theme = config['theme']
        load_theme(theme)

        # Seta página inicial
        self.registry_menu_clicked()

    def setup_data(self):
        """Carrega dados."""

        # Verifica conexão
        connected = self.database.connection_state == DatabaseConnection.State.CONNECTED

        # Se não houver conexão desabilita funções do aplicativo
        self.action_years.setDisabled(not connected)
        self.action_suppliers.setDisabled(not connected)
        self.action_import_backup.setDisabled(not connected)
        self.mp_main.setDisabled(not connected)

        # Carrega dados
        if connected:
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
            self.statusBar.showMessage(message)
        else:
            self.statusBar.clearMessage()

    @Slot()
    def handle_theme(self, theme: str):
        """Manipula tema"""
        config = get_config(ConfigSection.APP)
        config['theme'] = theme

        set_config(config, ConfigSection.APP)
        load_theme(theme)

    @Slot()
    def registry_menu_clicked(self):
        """Ativa página 'registrar'."""
        self.mp_main.setCurrentIndex(0)
        self.txt_nfe.setFocus()

    @Slot()
    def search_menu_clicked(self):
        """Ativa página 'pesquisar'."""
        self.mp_main.setCurrentIndex(1)
        self.txt_nfe_search.setFocus()
        self.handle_status_message(self.ID)

    # noinspection PyUnresolvedReferences
    @Slot()
    def export_menu_clicked(self):
        """Ativa página 'exportar'."""
        self.mp_main.setCurrentIndex(2)

        # Tentativa de burlar o bug visual da QWebView quando usa QAnimation para animar a transição
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.web_view.repaint())
        self.timer.setSingleShot(True)
        self.timer.start(300)

        self.handle_status_message(self.ID)

    @check_connection
    @Slot()
    def save_registry(self):
        """Cria ou edita registro no banco de dados."""

        # Define modo de interação
        mode = Mode.INSERT if self.ID == -1 else Mode.UPDATE

        fields = [
            self.txt_nfe,
            self.cb_date,
            self.cb_supplier,
            self.txt_value
        ]

        # Verifica se há campos em branco
        if not check_empty_fields(fields):
            Message.warning(self, 'ATENÇÃO', 'Preencha os campos obrigatórios!')
            return

        date = parse_date(self.cb_date.currentText(), '%d/%m/%Y')

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

        # Verifica se já existe um registro com a mesma nfe e fornecedor no banco de dados
        if self.database.exists(
                table='history',
                clause='WHERE nfe LIKE ? AND supplier LIKE ? AND id != ?',
                values=[fields['nfe'], fields['supplier'], self.ID]
        ):
            Message.warning(self, 'ATENÇÃO', 'Essa nota já foi registrada com esse fornecedor!')
            return

        message = 'Deseja {} esse registro no banco de dados?'
        message = message.format('inserir' if mode == Mode.INSERT else 'editar')

        # Faz pergunta de segurança ao usuário, caso não confirme aborta ação
        if Message.warning_question(self, message, Message.YES) == Message.NO:
            return

        # Caso fornecedor não se encontre no banco de dados, o adiciona
        if self.cb_supplier.findText(fields['supplier']) == -1:
            self.database.create(table='suppliers', fields={'supplier': fields['supplier']})
            self.load_suppliers()

        try:
            if mode == Mode.INSERT:
                self.database.create(table='history', fields=fields)
                message = 'Registro inserido com sucesso.'
            else:
                self.database.update(table='history', fields=fields, clause=f'WHERE id LIKE {self.ID}')
                message = 'Registro alterado com sucesso.'

            # Prepara para novo registro e avisa usuário
            Message.information(self, 'AVISO', message)
            self.registry_menu_clicked()
            self.new_registry()

            # Recarrega dados
            self.search()
            self.create_report()

            year = fields['date'].split('-')[0]
            print(year)

            if year != self.current_year:
                self.load_years()
        except QueryError:
            Message.critical(self, 'CRÍTICO', 'Algo deu errado durante a operação!')

    @Slot()
    def new_registry(self):
        """ Limpa campos da página registro."""
        fields = [
            self.txt_nfe,
            self.cb_date,
            self.cb_supplier,
            self.txt_value
        ]

        clear_fields(fields)
        self.txt_nfe.setFocus()

        self.ID = -1

    @check_connection
    @Slot()
    def delete_registry(self):
        """Deleta registro."""
        if Message.warning_question(self, 'Deseja deletar esse registro no banco de dados?') == Message.NO:
            return

        # Deleta registro
        try:
            self.database.delete(table='history', clause=f'WHERE id LIKE {self.ID}')

            # Prepara para novo registro e avisa usuário
            Message.information(self, 'AVISO', 'Registro deletado com sucesso.')
            self.registry_menu_clicked()

            # Recarrega dados
            self.search()
            self.create_report()
        except QueryError:
            Message.critical(self, 'CRÍTICO', 'Algo deu errado durante a operação!')

    @Slot()
    def edit_registry(self, index: QModelIndex | int):
        """Traz dados da QTableView para a página de registro."""
        # Pega linha clicada
        row = index.row() if isinstance(index, QModelIndex) else index
        model = self.table_search.model()

        # Obtém dados
        id_record = model.index(row, 0).data()
        nfe = model.index(row, 1).data()
        date = model.index(row, 2).data()
        supplier = model.index(row, 3).data()
        value = from_currency_to_float(model.index(row, 4).data())

        # Seta dados nos campos
        self.txt_nfe.setText(str(nfe))
        self.cb_date.setCurrentText(date)
        self.cb_supplier.lineEdit().setText(supplier)
        self.txt_value.setText(from_float_to_currency(value))

        # Entra em modo de edição
        self.ID = id_record
        self.registry_menu_clicked()

    @Slot()
    def clear_search(self):
        """Limpa campos da página de pesquisa."""
        self.txt_nfe_search.clear()
        self.txt_supplier_search.clear()
        self.cb_start_date.clear()
        self.cb_end_date.clear()

        self.txt_nfe_search.setFocus()

    @check_connection
    @Slot()
    def search(self):
        """Pesquisa dados no banco de dados e insere na QTableView."""
        nfe = self.txt_nfe_search.text()
        supplier = self.txt_supplier_search.text()
        start_date = parse_date(self.cb_start_date.currentText(), '%d/%m/%Y', on_fail=DateMinMax.MIN)
        end_date = parse_date(self.cb_end_date.currentText(), '%d/%m/%Y', on_fail=DateMinMax.MAX)

        # Realiza consulta
        query = self.database.read(
            table='history',
            fields=['id', 'nfe', 'date', 'supplier', 'value'],
            clause="WHERE nfe LIKE '%' || ? ||  '%' AND supplier LIKE '%' || ? || '%' "
                   "AND date >= ? AND date <= ? ORDER BY date",
            values=[nfe, supplier, start_date, end_date]
        )

        # Seta resultado da query ao model
        model = self.table_search.model()
        model.setQuery(query)

        # Seta headers do model
        model.setHeaderData(1, Qt.Orientation.Horizontal, 'NFE')
        model.setHeaderData(2, Qt.Orientation.Horizontal, 'DATA')
        model.setHeaderData(3, Qt.Orientation.Horizontal, 'FORNECEDOR')
        model.setHeaderData(4, Qt.Orientation.Horizontal, 'VALOR')

        # Esconde a coluna de ID e redimensiona colunas
        self.table_search.setColumnHidden(0, True)
        self.table_search.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

    @Slot()
    def export_pdf(self):
        """Exporta relatório em pdf."""
        if Message.warning_question(self, 'Deseja exportar o relatório em pdf?', Message.YES) == Message.NO:
            return

        # Abre caixa de diálogo para usuário selecionar local para salvar
        inicial_name = self.get_initial_filename()
        path = QFileDialog.getSaveFileName(self.centralwidget, 'Salvar em PDF.', inicial_name, 'pdf (*.pdf)')[0]

        # Caso usuário selecione um local, salva em pdf e informa usuário
        if path:
            self._export_pdf(path)
            Message.information(self, 'AVISO', 'Relatório exportado!')

    @Slot()
    def print_report(self):
        """Imprime relatório."""
        if Message.warning_question(self, 'Deseja imprimir o relatório?', Message.YES) == Message.NO:
            return

        filename = self.get_initial_filename()
        temp_file = os.path.join(os.getenv('temp'), filename)
        pdf_to_print_path = os.path.join(BASEDIR, 'bin', 'PDFtoPrinter.exe')

        self.temp_files.append(temp_file)
        self._export_pdf(temp_file)

        os.popen(fr'{pdf_to_print_path} "{temp_file}"')

    @check_connection
    @Slot()
    def create_report(self):
        """Cria relatório."""
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

            rows.append(
                {
                    'nfe': nfe,
                    'date': parse_date(date, input_format='%Y-%m-%d', output_format='%d/%b'),
                    'supplier': supplier,
                    'value': from_float_to_currency(value)
                }
            )

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

    @check_connection
    def load_years(self):
        """Carrega anos."""
        self.cb_year.blockSignals(True)

        years = self.database.get_years()
        self.cb_year.clear()
        self.cb_year.addItems(years)

        # Seta ano atual
        self.cb_year.setCurrentText(self.current_year)

        self.cb_year.blockSignals(False)

    @check_connection
    def load_suppliers(self):
        """Carrega fornecedores."""
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

    def get_initial_filename(self):
        """Retorna nome inicial do arquivo."""
        month = self.cb_month.currentText()
        year = self.cb_year.currentText()

        inicial_name = f'RELATÓRIO DE NOTAS {month} DE {year}.pdf'

        return inicial_name

    def _export_pdf(self, path: str):
        """
        Exporta pdf para o caminho passado.

        :param path: Caminho para exportar
        """
        layout = QPageLayout(
            QPageSize(QPageSize.PageSizeId.A4),
            QPageLayout.Orientation.Portrait,
            QMarginsF(0, 10, 0, 10)
        )

        self.web_view.printToPdf(path, layout)


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

        myappid = 'kamua.relatorio_de_notas.2.0.0'
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
        raise
