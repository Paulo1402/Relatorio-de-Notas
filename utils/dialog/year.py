from PyQt6.QtWidgets import QDialog

from ui.YearDialog import Ui_Dialog
from services import DatabaseConnection, get_years, delete_year
from utils import Message


class YearDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, database: DatabaseConnection):
        super().__init__(parent)
        self.setupUi(self)

        self.database = database

        years = get_years(self.database, force_current_year=False)

        self.cb_years.clear()
        self.cb_years.addItems(years)

        if self.cb_years.count() == 0:
            self.bt_delete.setDisabled(True)

        self.bt_delete.clicked.connect(self.delete)

    def delete(self):
        if Message.warning_question(
                self,
                'Deseja deletar TODOS os registros do ano selecionado?\nNão é possível reverter essa decisão.'
        ) == Message.StandardButton.No:
            return

        year = self.cb_years.currentText()
        delete_year(self.database, year)

        Message.information(self, 'AVISO', 'Registros deletados com sucesso.')
        self.cb_years.removeItem(self.cb_years.currentIndex())

        if self.cb_years.count() == 0:
            self.bt_delete.setDisabled(True)

        self.parent().setup_data()
