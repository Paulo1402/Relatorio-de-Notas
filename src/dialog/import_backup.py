from PySide6.QtWidgets import QDialog, QFileDialog

from ui.ImportBackupDialog import Ui_Dialog
from utils import Message
from services import DatabaseConnection, ImportBackupWorker


class ImportBackupDialog(QDialog, Ui_Dialog):
    """Diálogo para importar backup."""

    def __init__(self, parent, database: DatabaseConnection):
        super().__init__(parent)
        self.setupUi(self)

        self.database = database
        self.worker: ImportBackupWorker | None = None

        # Conecta signals
        self.bt_open.clicked.connect(self.open_file)
        self.bt_import.clicked.connect(self.handle_import_backup)
        self.txt_source.textChanged.connect(lambda: self.bt_import.setDisabled(self.txt_source.text() == ''))

        # Configura campos
        self.reset()

    def reset(self):
        """Reseta campos para o padrão."""
        self.progress_bar_main.setValue(0)
        self.progress_bar_table.setValue(0)
        self.txt_table.clear()
        self.txt_source.clear()

    def open_file(self):
        """Abre diálogo para selecionar backup."""
        path = QFileDialog.getExistingDirectory(self, 'Selecionar pasta de backup')

        if not path:
            return

        self.txt_source.setText(path)

    def handle_import_backup(self):
        """Importa backup."""

        # Se já houver um processo em andamento aborta a função
        if self.worker and self.worker.isRunning():
            Message.warning(self, 'ATENÇÃO', 'Aguarde o backup atual ser concluído!')
            return

        # Retorna dados dos campos
        source = self.txt_source.text()

        if Message.warning_question(
                self,
                f'Deseja importar os dados desse backup para dentro do banco de dados?\n'
                'Todos os dados atuais serão substituídos!'
        ) == Message.NO:
            return

        # Cria worker e conecta slots
        self.worker = ImportBackupWorker(self.database, source)
        self.worker.progress.connect(self.handle_progress)
        self.worker.success.connect(self.import_finished)
        self.worker.finished.connect(lambda: self.bt_import.setDisabled(False))
        self.worker.error.connect(self.handle_error)

        # Inicia worker
        self.worker.start()

        # Desabilita botão durante o processo
        self.bt_import.setDisabled(True)

    def handle_progress(self, progress: int, bar: str):
        """Exibe progresso do worker na barra de progresso"""
        if bar == 'main':
            self.progress_bar_main.setValue(progress)
        else:
            self.progress_bar_table.setValue(progress)
            self.txt_table.setText(bar)

    def handle_error(self, message: str):
        """Exibe erro e reseta campos."""
        Message.critical(self, 'CRÍTICO', message)

        self.reset()

    def import_finished(self):
        # Notifica usuário e recarrega dados no aplicativo
        Message.information(self, 'AVISO', f'Backup importado com sucesso.')

        self.parent().setup_data()

        # Reseta campos
        self.reset()
