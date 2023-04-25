from PyQt6.QtWidgets import QDialog

from ui.YearDialog import Ui_Dialog
from services import DatabaseConnection, get_years, delete_year
from utils import Message


# Diálogo para deletar anos no banco de dados
class YearDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, database: DatabaseConnection):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(160, 85)

        self.database = database

        # Pega anos dos dados
        years = get_years(self.database, force_current_year=False)

        self.cb_years.clear()
        self.cb_years.addItems(years)

        if self.cb_years.count() == 0:
            self.bt_delete.setDisabled(True)

        self.bt_delete.clicked.connect(self.delete)

    # Deleta ano
    def delete(self):
        if Message.warning_question(self, 'Deseja deletar TODOS os registros do ano selecionado?') == Message.NO:
            return

        # Deleta todos os dados do ano selecionado
        year = self.cb_years.currentText()
        delete_year(self.database, year)

        self.cb_years.removeItem(self.cb_years.currentIndex())

        if self.cb_years.count() == 0:
            self.bt_delete.setDisabled(True)

        Message.information(self, 'AVISO', 'Registros deletados com sucesso.')
        self.parent().load_years()
