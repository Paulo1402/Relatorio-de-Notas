from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtCore import QModelIndex, Qt

from utils import parse_date, from_float_to_currency


class Model(QSqlQueryModel):
    def __init__(self):
        super().__init__()

    def data(self, item: QModelIndex, role: int = ...):
        value = super().data(item, role)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        if role == Qt.ItemDataRole.DisplayRole:
            if item.column() == 2:
                return parse_date(value, input_format='%Y-%m-%d', output_format='%d/%m/%Y')

            if item.column() == 4:
                return from_float_to_currency(value)

            return value
