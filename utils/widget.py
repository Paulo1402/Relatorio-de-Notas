from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QFocusEvent

from utils import from_currency_to_float, from_float_to_currency


class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def focusInEvent(self, a0: QFocusEvent) -> None:
        value = from_currency_to_float(self.text())
        value = str(value).replace('.', ',')
        self.setText(value)

        super().focusInEvent(a0)

    def focusOutEvent(self, a0: QFocusEvent) -> None:
        value = from_currency_to_float(self.text())
        value = from_float_to_currency(value)
        self.setText(value)

        super().focusOutEvent(a0)
