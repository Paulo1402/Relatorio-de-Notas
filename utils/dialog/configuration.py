from PyQt6.QtWidgets import QDialog, QFileDialog
from PyQt6.QtGui import QCloseEvent

from ui.ConfigurationDialog import Ui_Dialog
from services import DatabaseConnection
from utils import set_config, get_config


# Diálogo para configurar banco de dados
class ConfigurationDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, dabase: DatabaseConnection):
        super().__init__(parent)
        self.setupUi(self)

        self.database = dabase

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
        config = get_config()

        self.database_path = config['database']
        backup = config['backup']

        frequency = backup['frequency']
        max_backups = backup['max_backups']

        self.txt_source.setText(self.database_path)

        self.set_checked_radio(self.frequency_radios, frequency)
        self.set_checked_radio(self.max_amount_radios, max_backups)

    @staticmethod
    def set_checked_radio(group_radio, radio_key):
        for key, radio in group_radio.items():
            if radio_key == key:
                radio.setChecked(True)

    @staticmethod
    def get_checked_radio(group_radio):
        for key, radio in group_radio.items():
            if radio.isChecked():
                return key

    # Salva configurações ao fehcar caixa de diálogo
    def closeEvent(self, a0: QCloseEvent):
        frequency = self.get_checked_radio(self.frequency_radios)
        max_backups = self.get_checked_radio(self.max_amount_radios)

        path = self.txt_source.text()

        config = {
            'database': path,
            'backup': {
                'frequency': frequency,
                'max_backups': max_backups
            }
        }
        set_config(config)

        # Caso haja alterações no caminho do banco de dados restabelece a conexão e recarrega dados
        if path != self.database_path:
            self.database.connect()
            self.parent().setup_data()

    # Abre caixa de diálogo para criar um arquivo
    def new_file(self):
        path = QFileDialog.getSaveFileName(self, 'Salvar banco de dados', filter='(*.sqlite)')[0]

        if not path:
            return

        with open(path, 'w', encoding='utf8'):
            pass

        self.txt_source.setText(path)

    # Abre caixa de diálogo para selecionar um arquivo
    def open_file(self):
        path = QFileDialog.getOpenFileName(self, 'Selecionar banco de dados', filter='(*.sqlite)')[0]

        if not path:
            return

        self.txt_source.setText(path)
