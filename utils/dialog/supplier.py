from PyQt6.QtWidgets import QDialog

from ui.SupplierDialog import Ui_Dialog
from services import DatabaseConnection
from utils import Message, ListModel


class SupplierDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, database: DatabaseConnection):
        super().__init__(parent)
        self.setupUi(self)

        self.database = database

        self.model = ListModel()
        self.list_suppliers.setModel(self.model)

        self.bt_search.setShortcut('Return')

        self.bt_search.clicked.connect(self.search)
        self.bt_delete.clicked.connect(self.delete)

        self.search()

    def search(self):
        supplier = self.txt_supplier.text()

        query = self.database.read(
            table='suppliers',
            fields=['supplier'],
            where={
                'clause': "WHERE supplier LIKE '%' || ? ||  '%' ORDER BY supplier",
                'values': [supplier]
            }
        )

        self.model.setQuery(query)

    def delete(self):
        if Message.warning_question(
                self,
                'Deseja deletar TODOS os registros selecionados?\nNão é possível reverter essa decisão.'
        ) == Message.StandardButton.No:
            return

        indexes = self.list_suppliers.selectedIndexes()

        for index in indexes:
            self.database.delete(table='suppliers', clause=f'WHERE supplier LIKE "{index.data()}"')

        self.search()
        self.parent().setup_data()
