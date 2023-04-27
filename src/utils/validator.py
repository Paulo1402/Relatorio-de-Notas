"""Validadores de campos."""

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator

from . import from_float_to_currency, from_currency_to_float, get_today


class DateValidator(QRegularExpressionValidator):
    """Validador para campos de data."""

    def __init__(self):
        super().__init__()

        self.state = self.State.Invalid

        regex = QRegularExpression(r'(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[12])/[12][0-9]{3}')
        self.setRegularExpression(regex)

    def validate(self, input_text: str, pos: int) -> tuple:
        """
        Valida o campo.

        Esse método é chamado automaticamente quando algo é digitado no campo.
        O método foi sobreposto apenas para salvar o resultado da validação no escopo da classe para futura
        verificação.

        :param input_text: Texto de entrada
        :param pos: Posição do caractere
        :return: Tupla com texto, posição e resultado da validação
        """
        result: tuple = super().validate(input_text, pos)
        self.state = result[0]

        return result

    def fixup(self, input_text: str) -> str:
        """
        Seta autoformat.

        Esse método é chamado automaticamente para tentar autovalidar um campo quer perdeu o foco e que ainda não
        foi validado.

        :param input_text: Texto de entrada
        :return: Texto manipulado
        """
        regex = QRegularExpression(r'(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[12])')
        match = regex.match(input_text)

        if not match.hasMatch():
            return

        year = get_today(output='/%Y')
        input_text += year

        return input_text
