from PyQt6.QtWidgets import QMessageBox, QWidget


class Message(QMessageBox):
    def __init__(
            self,
            parent: QWidget | None = None,
            buttons: list[tuple[QMessageBox.StandardButton, str]] | None = None,
    ):
        super().__init__(parent)

        if buttons:
            self.setCaptionButtons(buttons)

    def show_message(
            self, title: str,
            message: str,
            icon: QMessageBox.Icon | None = None,
            default_button: QMessageBox.StandardButton | None = None
    ):
        self.setWindowTitle(title)
        self.setText(message)
        self.setIcon(icon)
        self.setDefaultButton(default_button)

        return super().exec()

    def setCaptionButtons(self, buttons: list[tuple[QMessageBox.StandardButton, str]]):
        b = 0

        for button, _ in buttons:
            b |= button

        self.setStandardButtons(b)

        for button, caption in buttons:
            self.button(button).setText(caption)
