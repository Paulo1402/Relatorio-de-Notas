from PyQt6.QtWidgets import QMessageBox, QWidget


class Message(QMessageBox):
    def __init__(
            self,
            parent: QWidget,
            title: str,
            message: str,
            icon: QMessageBox.Icon,
            buttons: list[tuple[QMessageBox.StandardButton, str]],
            default_button: QMessageBox.StandardButton | None = None
    ):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(icon)

        b = 0

        for button, _ in buttons:
            b |= button

        self.setStandardButtons(b)
        self.setDefaultButton(default_button)

        for button, caption in buttons:
            self.button(button).setText(caption)


