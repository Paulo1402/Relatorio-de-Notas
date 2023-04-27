from datetime import datetime

from . import DateMinMax


def parse_date(
        date: str,
        input_format: str,
        output_format: str = '%Y-%m-%d',
        on_fail: DateMinMax | None = None
) -> str | None:
    """
    Formata uma data de um formato de entrada para o formato de saída.

    :param date: Data como string
    :param input_format: Formato de entrada
    :param output_format: Formato de saída
    :param on_fail: Tentar converter para outro formato caso algum erro aconteça
    :return: Data formatada ou None caso 'on_fail' não seja enviado
    """
    try:
        parsed_date = datetime.strptime(date, input_format)
        parsed_date = parsed_date.strftime(output_format)
    except (ValueError, TypeError):
        parsed_date = None

        if on_fail == DateMinMax.MIN:
            parsed_date = datetime.min.strftime(output_format)
        elif on_fail == DateMinMax.MAX:
            parsed_date = datetime.max.strftime(output_format)

    return parsed_date


def from_float_to_currency(value: float | int, symbol: bool = True) -> str:
    """
    Formata float para string formatada.

    :param value: Valor como float ou int
    :param symbol: Adicionar símbolo
    :return: Valor formatado como moeda
    """
    value = f'{value:_.2f}'
    value = value.replace('.', ',').replace('_', '.')

    if symbol:
        value = 'R$ ' + value

    return value


def from_currency_to_float(value: str) -> float:
    """
    Formata de string formatada para float.

    :param value: Valor como str
    :return: Valor como float
    """
    value = value.replace('R$', '').replace('.', '').replace(',', '.')
    value = float(value) if value != '' else 0

    return value
