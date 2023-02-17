import calendar
from datetime import datetime
from enum import Enum


# Enumeração para a função parse_date
class DateMinMax(Enum):
    MIN = 1
    MAX = 2


# Formata uma data de um formato de entrada para o formato de saída
def parse_date(date: str, input_format: str, output_format: str = '%Y-%m-%d', on_fail: DateMinMax | None = None):
    try:
        parsed_date = datetime.strptime(date, input_format)
        parsed_date = parsed_date.strftime(output_format)
    except ValueError:
        if on_fail == DateMinMax.MIN:
            parsed_date = datetime.min.strftime(output_format)
        elif on_fail == DateMinMax.MAX:
            parsed_date = datetime.max.strftime(output_format)
        else:
            parsed_date = None

    return parsed_date


# Retorna primeiro e último dia do mês formatados de acordo com ano e mês de referência
def parse_month(month: int, year: int):
    first_day = f'{year}-{month:02d}-01'
    last_day = calendar.monthrange(year, month)[1]

    last_day = f'{year}-{month:02d}-{last_day}'

    return first_day, last_day


# Formata float para string formatada
def from_float_to_currency(value: float | int):
    value = f'R$ {value:_.2f}'
    value = value.replace('.', ',').replace('_', '.')

    return value


# Formata de string formatada para float
def from_currency_to_float(value: str):
    value = value.replace('R$', '').replace('.', '').replace(',', '.')
    value = float(value) if value != '' else 0

    return value
