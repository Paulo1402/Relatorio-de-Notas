"""Funções gerais usadas ao longo do programa."""
import calendar
from datetime import datetime
from jinja2 import Template

import qdarktheme
from PySide6.QtWidgets import QLineEdit, QComboBox

from . import Message, DARK_COLOR, LIGHT_COLOR
from services import DatabaseConnection


def check_empty_fields(fields: list[QLineEdit | QComboBox]) -> bool:
    """
    Verifica se há campos em branco.

    Caso o campo esteja em branco atualiza o QSS para destacá-lo e coloca em foco o
    primeiro campo.

    :param fields: Lista de campos.
    :return: True se houver campos em branco e False se não houver.
    """
    empty_fields = []

    for field in fields:
        value = field.currentText() if isinstance(field, QComboBox) else field.text()

        # Se estiver vazio
        if not value.strip():
            empty_fields.append(field)

            # Atualiza QSS
            field.setProperty('class', 'required')
            field.style().polish(field)

    if empty_fields:
        empty_fields[0].setFocus()
        return False

    return True


def is_date_range_valid(start_date: str, end_date: str, date_format='%Y-%m-%d') -> bool:
    """
    Checa se a data inicial é menor que a data final.

    :param start_date: Data inicial
    :param end_date: Data final
    :param date_format: Formato da data enviada
    :return: True | False
    """
    start_date_parsed = datetime.strptime(start_date, date_format)
    end_date_parsed = datetime.strptime(end_date, date_format)

    return start_date_parsed <= end_date_parsed


def get_current_month_year() -> tuple[int, int]:
    """
    Retorna mês e ano atual.

    :return: Mês e ano como int
    """
    today = datetime.today()

    return today.month, today.year


def get_months_name() -> list[str]:
    months = [month.upper() for month in calendar.month_name]

    return months


def get_today(output: str = '%Y-%m-%d') -> str:
    """
    Retorna data de hoje como string.

    :param output: Formato de saída
    :return: Data formatada
    """
    today = datetime.today().date()

    return today.strftime(output)


def get_range_month(month: int, year: int) -> tuple[str, str]:
    """
    Retorna primeiro e último dia do mês formatados de acordo com ano e mês de referência.

    :param month: Mês de referência
    :param year: Ano de referência
    :return: Tupla com primeiro e último dia do mês.
    """
    first_day = f'{year}-{month:02d}-01'
    last_day = calendar.monthrange(year, month)[1]

    last_day = f'{year}-{month:02d}-{last_day}'

    return first_day, last_day


def create_html(data: dict) -> str:
    """
    Cria html do relatório dinamicamente.

    :param data: Dicionário com dados
    :return: HTML como string
    """
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


def clear_fields(fields: list[QLineEdit | QComboBox]):
    """
    Reseta valores e QSS dos campos para o padrão.

    :param fields: Lista de campos
    """
    for field in fields:
        if isinstance(field, QComboBox):
            field.setCurrentIndex(0)
        else:
            field.clear()

        # Atualiza QSS
        field.setProperty('class', '')
        field.style().polish(field)


def load_theme(theme: str):
    """
    Carrega tema.

    Carrega e configura tema, além de adicionar regras QSS adicionais.

    :param theme: Tema a ser carregado
    """
    if theme == 'light':
        border_color = 'black'
    else:
        border_color = 'white'

    qss = '''
        QPushButton:hover{
            border: 1px solid %s;
        }

        QLineEdit[class="required"],
        QComboBox[class="required"]{
             border: 1px solid red;
        }

        QGroupBox{
            margin: 0;
        } 
    ''' % border_color

    custom_colors = {
        '[dark]': {
            'primary': DARK_COLOR
        },
        '[light]': {
            'primary': LIGHT_COLOR
        }
    }

    qdarktheme.setup_theme(
        theme=theme,
        custom_colors=custom_colors,
        additional_qss=qss
    )


def check_connection(func):
    """
    Checa conexão com banco de dados antes de executar uma função.

    Decorar a função desejada com essa função.

    :param func: A função que deve ser checada
    :return: Uma nova função para ser executada no lugar da função original
    """

    def inner(self, *args, **kwargs):
        database: DatabaseConnection = self.database

        if not database.check_location(database.location):
            Message.critical(self, 'CRÍTICO', 'Sem conexão com o banco de dados!')
            return

        func(self, *args, **kwargs)

    return inner
