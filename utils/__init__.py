import locale
from datetime import datetime

from PyQt6.QtWidgets import QLineEdit, QComboBox
from jinja2 import Template

from utils.parse import DateMinMax, parse_date, parse_month, from_float_to_currency, from_currency_to_float
from utils.config import get_config, set_config, BASEDIR
from utils.model import TableModel, ListModel
from utils.widget import CustomLineEdit, Message
from utils.dialog import *

__all__ = [
    'DateMinMax',
    'parse_date',
    'parse_month',
    'from_float_to_currency',
    'from_currency_to_float',
    'get_empty_fields',
    'create_html',
    'get_current_month_year',
    'get_config',
    'set_config',
    'BASEDIR',
    'ConfigurationDialog',
    'YearDialog',
    'SupplierDialog',
    'CalendarDialog',
    'ImportBackupDialog',
    'TableModel',
    'ListModel',
    'Message',
]

# Define localização para usar a biblioteca datetime
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')


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
