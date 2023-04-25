from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtCore import QModelIndex, Qt

from utils import parse_date, from_float_to_currency


# Model personalizado para tratar dados antes de adicionar a QTableView
class TableModel(QSqlQueryModel):
    def data(self, item: QModelIndex, role: int = ...):
        # Retorna valor original
        value = super().data(item, role)

        # Alinha todos objetos ao centro
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        if role == Qt.ItemDataRole.DisplayRole:
            # Caso seja coluna de datas, formata o valor para data brasileira
            if item.column() == 2:
                return parse_date(value, input_format='%Y-%m-%d', output_format='%d/%m/%Y')

            # Caso seja coluna de valor, formata o valor para moeda brasileira
            if item.column() == 4:
                return from_float_to_currency(value)

            return value


class ListModel(QSqlQueryModel):
    def data(self, item: QModelIndex, role: int = ...):
        # Alinha todos objetos ao centro
        # if role == Qt.ItemDataRole.TextAlignmentRole:
        #     return Qt.AlignmentFlag.AlignLeft

        if role == Qt.ItemDataRole.DisplayRole:
            return super().data(item, role)
