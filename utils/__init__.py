import locale
from calendar import monthrange
from datetime import datetime
from enum import Enum

from jinja2 import Template
from bs4 import BeautifulSoup
from PyQt6.QtWidgets import QLineEdit, QComboBox

__all__ = [
    'Mode',
    'DateMinMax',
    'parse_date',
    'parse_month',
    'from_float_to_currency',
    'from_currency_to_float',
    'get_empty_fields',
    'create_html'
]

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


class Mode(Enum):
    INSERT = 1
    UPDATE = 2


class DateMinMax(Enum):
    MIN = 1
    MAX = 2


def parse_date(date: str, input_format: str, output_format: str, on_fail: DateMinMax | None = None):
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


def parse_month(month_ref: int):
    first_day = f'2023-{month_ref:02d}-01'
    last_day = monthrange(2023, month_ref)[1]

    last_day = f'2023-{month_ref:02d}-{last_day}'

    return first_day, last_day


def from_float_to_currency(value: float | int):
    value = f'R$ {value:_.2f}'
    value = value.replace('.', ',').replace('_', '.')

    return value


def from_currency_to_float(value: str):
    value = value.replace('R$', '').replace('.', '').replace(',', '.')
    value = float(value)

    return value


def get_empty_fields(fields: list[QLineEdit | QComboBox]):
    empty_fields = []

    for field in fields:
        if type(field) == QLineEdit:
            if field.text().strip() == '':
                empty_fields.append(field)
        else:
            if field.currentText().strip() == '':
                empty_fields.append(field)

    return empty_fields


def create_html(data: dict):
    template = '''
    <h1>MADEIREIRA KAMUA LTDA</h1>
    <h2>RELATÓRIO DE NOTAS {{ month }} {{ year }} </h2>
    <table>
        <thead>
            <tr>
                <th>NOTA</th>
                <th>DATA</th>
                <th>FORNECEDOR</th>
                <th>VALOR</th>
            </tr>
        </thead>
        <tbody>
            {% for row in rows %}
            <tr>
                <td>{{ row['nfe'] }}</td>
                <td>{{ row['date'] }}</td>
                <td>{{ row['supplier'] }}</td>
                <td>{{ row['value'] }}</td>
            </tr>
            {% endfor %}
        </tbody>
        <tfoot>
            <tr>
                <td></td>
                <td></td>
                <td></td>
                <td>{{ total }}</td>
            </tr>
        </tfoot>
    </table>
    '''

    with open('utils/templates/report.html', 'r', encoding='utf-8') as f:
        html = BeautifulSoup(f.read(), 'html.parser')

    body = Template(template).render(**data)
    body_parsed = BeautifulSoup(body, 'html.parser')

    html.find('body').append(body_parsed)

    return html.prettify()
