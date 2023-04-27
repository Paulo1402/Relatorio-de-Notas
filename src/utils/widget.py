"""
Módulo usado para criar CustomWidgets com funcionalidades extras.

Esse módulo é importado em 'ui./MainWindow.py' para aplicar os widgets customizados.
"""

from PySide6.QtWidgets import QLineEdit, QComboBox, QStackedWidget, QGraphicsOpacityEffect
from PySide6.QtCore import QEasingCurve, QRect
from PySide6.QtGui import QFocusEvent

from . import from_currency_to_float, from_float_to_currency, Animation
from dialog import CalendarDialog


class CustomComboBox(QComboBox):
    """Subclasse de QComboBox para abrir um popup para selecionar uma data quando interagir com o drop down arrow."""

    def __init__(self, parent):
        super().__init__(parent)

        self.animation: Animation | None = None
        self.popup: CalendarDialog | None = None

    def showPopup(self):
        self.popup = CalendarDialog(self.parent(), self)
        self.popup.show()

        geo = self.popup.geometry()

        self.animation = Animation(
            widget=self.popup,
            property_name=b'geometry',
            start=QRect(geo.x(), geo.y(), geo.width(), 1),
            end=QRect(geo.x(), geo.y(), geo.width(), geo.height()),
            duration=250,
            easing_curve=QEasingCurve.Type.InCirc
        )


class CustomLineEdit(QLineEdit):
    """LineEdit com autoformatar moeda."""

    def __init__(self, parent=None):
        super().__init__(parent)

    # Formata para float ao receber o foco
    def focusInEvent(self, a0: QFocusEvent) -> None:
        value = from_currency_to_float(self.text())
        value = str(value).replace('.', ',')
        self.setText(value)

        super().focusInEvent(a0)

    # Formata para moeda ao perder o foco
    def focusOutEvent(self, a0: QFocusEvent) -> None:
        value = from_currency_to_float(self.text())
        value = from_float_to_currency(value)
        self.setText(value)

        super().focusOutEvent(a0)


class CustomStackedWidget(QStackedWidget):
    """Subclasse de QStackedWidget para adicionar uma animação de fade in em transições."""

    def __init__(self, parent):
        super().__init__(parent)

        self.animation: Animation | None = None

    def setCurrentIndex(self, index: int):
        if index == self.currentIndex():
            return

        super().setCurrentIndex(index)

        widget = self.currentWidget()
        opacity_effect = QGraphicsOpacityEffect(self)
        widget.setGraphicsEffect(opacity_effect)

        self.animation = Animation(
            widget=opacity_effect,
            property_name=b'opacity',
            start=0,
            end=1,
            duration=250,
            easing_curve=QEasingCurve.Type.InQuad
        )
