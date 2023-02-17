from PyQt6.QtWidgets import QLineEdit, QMessageBox
from PyQt6.QtGui import QFocusEvent

from utils import from_currency_to_float, from_float_to_currency


# Template de QMessageBox com captions personalizados para botões
class Message(QMessageBox):
    def __init__(
            self,
            parent=None,
            buttons: list[tuple[QMessageBox.StandardButton, str]] | None = None,
    ):
        super().__init__(parent)

        if buttons:
            self.set_caption_buttons(buttons)

    @classmethod
    def warning_question(cls, parent, message):
        buttons = [(QMessageBox.StandardButton.Yes, 'Sim'), (QMessageBox.StandardButton.No, 'Não')]

        self = cls(parent, buttons)
        answer = self.show_message(
            'ATENÇÃO',
            message,
            QMessageBox.Icon.Warning,
            QMessageBox.StandardButton.No
        )

        return answer

    # Executa MessageBox
    def show_message(
            self,
            title: str,
            message: str,
            icon: QMessageBox.Icon | None = None,
            default_button: QMessageBox.StandardButton | None = None
    ):
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(icon)
        self.setDefaultButton(default_button)

        return super().exec()

    # Seta captions personalizados
    def set_caption_buttons(self, buttons: list[tuple[QMessageBox.StandardButton, str]]):
        b = 0

        for button, _ in buttons:
            b |= button

        self.setStandardButtons(b)

        for button, caption in buttons:
            self.button(button).setText(caption)


# LineEdit com auto formatar moeda
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
