"""
Módulo usado para criar CustomWidgets com funcionalidades extras.

Esse módulo é importado em 'ui./MainWindow.py' para aplicar os widgets customizados.
"""

import re

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

        self.textChanged.connect(self.format_currency)

    # Formata para float ao receber o foco
    # def focusInEvent(self, a0: QFocusEvent) -> None:
    #     value = from_currency_to_float(self.text())
    #     value = str(value).replace('.', ',')
    #     self.setText(value)
    #
    #     super().focusInEvent(a0)
    #
    # Formata para moeda ao perder o foco
    # def focusOutEvent(self, a0: QFocusEvent) -> None:
    #     value = from_currency_to_float(self.text())
    #     value = from_float_to_currency(value)
    #     self.setText(value)
    #
    #     super().focusOutEvent(a0)

    def format_currency(self, value):
        value = re.sub(r"\D", "", value)

        if not value:
            self.setText('')
            return

        value = str(int(value))

        match len(value):
            case 1:
                point_number = '00' + value
            case 2:
                point_number = '0' + value
            case 3 | 4 | 5:
                point_number = value
            case 6 | 7 | 8:
                point_number = f'{value[:len(value) - 5]}.{value[-5:]}'
            case 9 | 10 | 11:
                point_number = self.insert_point(8, value)
            case 12 | 13 | 14:
                point_number = self.insert_point(11, value)
            case _:
                self.setText('R$ 0,00')
                return

        comma_number = f'R$ {point_number[:len(point_number) - 2]},{point_number[-2:]}'

        # Evita chamar o método outra vez ao setar o valor formatado
        self.blockSignals(True)
        self.setText(comma_number)
        self.blockSignals(False)

    @staticmethod
    def insert_point(start, value):
        """Insere separador de milhar."""
        i = value[:len(value) - start]
        m1 = value[-start:][:3]
        m2 = value[-8:][:3]
        f = value[-5:]

        if (m2 == m1) and (len(value) < 12):
            return f'{i}.{m1}.{f}'
        else:
            return f'{i}.{m1}.{m2}.{f}'


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
            easing_curve=QEasingCurve.Type.InQuad,
        )
