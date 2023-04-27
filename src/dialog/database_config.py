import os
from pathlib import Path

from PySide6.QtWidgets import QDialog, QFileDialog
from PySide6.QtGui import QCloseEvent

from ui.DatabaseConfigDialog import Ui_Dialog
from utils import set_config, get_config, ConfigSection, Message
from services import DatabaseConnection


class DatabaseConfigDialog(QDialog, Ui_Dialog):
    """Diálogo para configurar banco de dados."""

    def __init__(self, parent, database: DatabaseConnection):
        super().__init__(parent)
        self.setupUi(self)

        self.database = database
        self.root = str(Path.home())

        self.frequency_radios = {
            'no_backups': self.radio_no_backup,
            'diary': self.radio_diary,
            'weekly': self.radio_weekly,
            'monthly': self.radio_monthly
        }

        self.max_amount_radios = {
            3: self.radio_3,
            5: self.radio_5,
            10: self.radio_10
        }

        self.bt_open.clicked.connect(self.open_file)
        self.bt_new.clicked.connect(self.new_file)
        self.radio_no_backup.toggled.connect(self.group_max_backup.setDisabled)
        self.txt_source.textChanged.connect(lambda: self.frame_backup.setDisabled(self.txt_source.text() == ''))

        self.group_max_backup.setDisabled(True)
        self.frame_backup.setDisabled(True)

        # Retorna configurações atuais e seta na interface
        self.config = get_config(ConfigSection.DATABASE)

        self.database_path = self.config['name']

        frequency = self.config['backup_frequency']
        max_backups = self.config['max_backups']

        self.txt_source.setText(self.database_path)
        self.set_checked_radio(self.frequency_radios, frequency)
        self.set_checked_radio(self.max_amount_radios, max_backups)

    @staticmethod
    def set_checked_radio(group_radio: dict, radio_key: str):
        """Seta radio pela key."""
        for key, radio in group_radio.items():
            if radio_key == key:
                radio.setChecked(True)

    @staticmethod
    def get_checked_radio(group_radio: dict) -> str:
        """Retorna checked radio."""
        for key, radio in group_radio.items():
            if radio.isChecked():
                return key

    def closeEvent(self, event: QCloseEvent):
        """Salva configurações ao fechar caixa de diálogo."""
        path = self.txt_source.text()
        frequency = self.get_checked_radio(self.frequency_radios)
        max_backups = self.get_checked_radio(self.max_amount_radios)

        self.config['name'] = path
        self.config['backup_frequency'] = frequency
        self.config['max_backups'] = max_backups

        set_config(self.config, ConfigSection.DATABASE)

        # Caso haja alterações no caminho do banco de dados restabelece a conexão e recarrega dados
        if path != self.database_path:
            self.database.connect()
            self.parent().setup_data()

        event.accept()

    def new_file(self):
        """Abre caixa de diálogo para criar um diretório."""

        path = QFileDialog.getExistingDirectory(self, 'Selecione um diretório para salvar', self.root)

        if not path:
            return

        path = Path(path)

        if len(os.listdir(path)) > 0:
            Message.warning(self, 'ATENÇÃO', 'O diretório precisa estar vazio! Crie uma nova pasta nesse local e '
                                             'a selecione.')
            return

        try:
            database = path / 'db.sqlite'
            backups = path / 'backups'

            database.touch()
            backups.mkdir()
        except PermissionError:
            Message.warning(self, 'ATENÇÃO', 'O diretório especificado possui restrições para escrita! Por favor '
                                             'selecione outro.')
            return

        self.txt_source.setText(str(path))

    def open_file(self):
        """Abre caixa de diálogo para selecionar um arquivo."""
        path = QFileDialog.getOpenFileName(self, 'Selecionar banco de dados', self.root, filter='(*.sqlite)')[0]

        if not path:
            return

        self.txt_source.setText(path)
