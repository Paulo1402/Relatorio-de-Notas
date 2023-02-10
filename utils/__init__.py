import locale
import os
from calendar import monthrange
from datetime import datetime
from enum import Enum

from jinja2 import Template
from PyQt6.QtWidgets import QLineEdit, QComboBox

__all__ = [
    'DateMinMax',
    'parse_date',
    'parse_month',
    'from_float_to_currency',
    'from_currency_to_float',
    'get_empty_fields',
    'create_html',
    'get_current_month_year',
    'BASEDIR'
]

# Caminho relativo ao main.py
BASEDIR = os.path.dirname(os.path.dirname(__file__))

# Define localização para usar a biblioteca datetime
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


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
    last_day = monthrange(year, month)[1]

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


# Retorna campos em branco
def get_empty_fields(fields: list[QLineEdit | QComboBox]):
    empty_fields = []

    for field in fields:
        if isinstance(field, QComboBox):
            if field.currentText().strip() == '':
                empty_fields.append(field)
        else:
            if field.text().strip() == '':
                empty_fields.append(field)

    return empty_fields


def get_current_month_year():
    today = datetime.today()

    return today.month, today.year


# Cria html dinamicamente de acordo com parâmetros
def create_html(data: dict):
    template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>RELATÓRIO DE NOTAS</title>
        <style>
          body {
            font-family: Bookman Old Style;
            font-weight: bold;
            font-style: italic;
    
            text-align: center;
            width: 500px;
            margin: auto;
          }
    
          h1,
          h2 {
            font-size: 15px;
          }
    
          table {
            margin-top: 25px;
            margin-bottom: 20px;
            border-collapse: collapse;
            width: 500px;
    
            page-break-inside: auto;
          }
    
          thead {
            font-size: 14px;
            background-color: black;
            color: white;
    
            display: table-header-group;
          }
    
          tbody {
            font-family: Calibri;
            font-size: 14px;
            font-weight: normal;
            font-style: normal;
          }
    
          tfoot {
            display: table-row-group;
          }
    
          tr {
            page-break-inside: avoid;
            page-break-after: auto;
          }
    
          td,
          th {
            border: 1px solid black;
            padding: 5px;
          }
    
          tr:nth-child(even) {
            background-color: #dddddd;
          }
    
          tfoot tr,
          tfoot td:nth-child(-n + 3) {
            background-color: none;
            border: none;
          }
    
          tfoot td:nth-last-child(1) {
            background-color: yellow;
            font-size: 13px;
          }
        </style>
    </head>
    <body>
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
    </body>
    </html>
   '''

    # Caso não haja dados adiciona campos vazios para uma melhor visualização
    if not data['rows']:
        rows = [{'nfe': '', 'date': '', 'supplier': '', 'value': ''}]
        data['rows'] = rows

    # Formata template com base nos dados enviados
    html = Template(template).render(**data)

    return html
