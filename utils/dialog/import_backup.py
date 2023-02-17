import csv

from PyQt6.QtWidgets import QDialog, QFileDialog

from ui.ImportBackupDialog import Ui_Dialog
from services import DatabaseConnection
from utils import Message


class ImportBackupDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, database: DatabaseConnection):
        super().__init__(parent)
        self.setupUi(self)

        self.database = database

        self.bt_open.clicked.connect(self.open_file)
        self.bt_import.clicked.connect(self.import_backup)
        self.txt_source.textChanged.connect(lambda: self.bt_import.setDisabled(self.txt_source.text() == ''))

        self.cb_table.addItems(['history', 'suppliers'])
        self.bt_import.setDisabled(True)

    def open_file(self):
        path = QFileDialog.getOpenFileName(self, 'Selecionar backup', filter='(*.csv)')[0]

        if not path:
            return

        self.txt_source.setText(path)

    def import_backup(self):
        table = self.cb_table.currentText()
        source = self.txt_source.text()

        if Message.warning_question(
                self,
                f'Deseja importar esses dados para dentro da tabela {table}?'
        ) == Message.StandardButton.No:
            return

        with open(source, 'r', encoding='latin') as f:
            reader = csv.reader(f, delimiter=';')

            header_flag = True
            header = None

            for row in reader:
                if header_flag:
                    header = row
                    header_flag = False
                    continue

                fields = {field: value for field, value in list(zip(header, row))}

                self.database.create(
                    table=table,
                    fields=fields
                )

        Message.information(self, 'AVISO', f'Backup da tabela {table} importada com sucesso.')
