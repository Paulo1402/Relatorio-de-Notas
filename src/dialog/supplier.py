from PySide6.QtWidgets import QDialog

from ui.SupplierDialog import Ui_Dialog
from utils import Message, ListModel
from services import DatabaseConnection


# Diálogo para deletar fornecedores do banco de dados
class SupplierDialog(QDialog, Ui_Dialog):
    def __init__(self, parent, database: DatabaseConnection):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(390, 305)

        self.database = database

        self.model = ListModel()
        self.list_suppliers.setModel(self.model)

        self.bt_search.setShortcut('Return')

        self.bt_search.clicked.connect(self.search)
        self.bt_delete.clicked.connect(self.delete)

        self.search()

    # Filtra pelo nome do fornecedor
    def search(self):
        supplier = self.txt_supplier.text()

        query = self.database.read(
            table='suppliers',
            fields=['supplier'],
            clause="WHERE supplier LIKE  '%' || ? ||  '%' ORDER BY supplier",
            values=[supplier]
        )

        self.model.setQuery(query)

    # Deleta fornecedor
    def delete(self):
        # Pega todos os índices selecionados
        indexes = self.list_suppliers.selectedIndexes()

        if not indexes:
            return

        if Message.warning_question(self, 'Deseja deletar TODOS os registros selecionados?') == Message.NO:
            return

        # Para cada índice selecionado, deleta fornecedor
        for index in indexes:
            supplier = index.data()
            self.database.delete(table='suppliers', clause=f'WHERE supplier LIKE "{supplier}"')

        self.search()

        # Avisa usuário e recarrega dados dos fornecedores no aplicativo
        Message.information(self, 'AVISO', 'Registros deletados com sucesso.')
        self.parent().load_suppliers()
