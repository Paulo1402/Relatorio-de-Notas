import os
import csv
import json
import shutil
from datetime import datetime
from collections import namedtuple

from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtSql import QSqlQuery

from services.connection import DatabaseConnection, QueryError
from utils import get_config

__all__ = [
    'DatabaseConnection',
    'QueryError',
    'get_years',
    'delete_year',
    'check_connection',
    'do_backup'
]


# Retorna anos dos dados
def get_years(database: DatabaseConnection, force_current_year: bool = True):
    query = QSqlQuery(database.connection)
    query.exec("SELECT DISTINCT strftime('%Y', date) FROM history ORDER BY date")

    years = []

    while query.next():
        years.append(query.value(0))

    if not years and force_current_year:
        current_year = str(datetime.today().year)
        years.append(current_year)

    return years


# Deleta todos os registros de um ano específico
def delete_year(database: DatabaseConnection, year: str):
    query = QSqlQuery(database.connection)
    query.exec(f"DELETE FROM history WHERE strftime('%Y', date) LIKE {year}")


# Checa conexão com banco de dados antes de executar uma função que requer conexão
def check_connection(func):
    def inner(self, *_, **__):
        if self.database.connection_state != DatabaseConnection.State.CONNECTED:
            QMessageBox.critical(self, 'CRÍTICO', 'Sem conexão com o banco de dados!')
            return

        func(self)

    return inner


# Realiza o backup do banco de dados em arquivos .csv
def do_backup(database: DatabaseConnection):
    # Cria arquivo csv com dados da tabela
    def write_csv(filename: str, header: list, query: QSqlQuery):
        with open(filename, 'w', encoding='utf8') as f:
            writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
            writer.writerow(header)

            while query.next():
                values = [query.value(i) for i in range(len(header))]
                writer.writerow(values)

    # Pega as configurações do aplicativo
    config = get_config()

    db = config['database']
    backup = config['backup']

    frequency = backup['frequency']
    max_backups = backup['max_backups']

    # Caso não haja um banco de dados configurado ou 'no_backups' está setado aborta backup
    if not db or frequency == 'no_backups':
        return

    # Pega raíz da pasta de backups
    root = os.path.join(os.path.dirname(db), 'backups')

    # Cria raíz caso não exista
    if not os.path.exists(root):
        os.makedirs(root)

    # Pega o arquivo de configuração da pasta de backup
    backup_config_path = os.path.join(root, 'config.json')

    # Tenta coletar data do último backup e transforma em um objeto datetime
    try:
        with open(backup_config_path, 'r', encoding='utf8') as f:
            config = json.loads(f.read())

            last_backup = config['last_backup']
            last_backup = datetime.strptime(last_backup, '%Y-%m-%d')
    except (FileNotFoundError, KeyError, ValueError, json.JSONDecodeError):
        last_backup = None

    # Retona data atual
    today = datetime.today().date()

    # Verifica se há necessidade de realizar o backup com base na configuração 'frequency'
    if last_backup:
        if frequency == 'diary':
            if last_backup == today:
                return
        elif frequency == 'weekly':
            if last_backup.isocalendar().week == today.isocalendar().week:
                return
        else:
            if last_backup.month == today.month:
                return
    else:
        last_backup = today

    # Transforma datetime em string novamente
    last_backup = last_backup.strftime('%Y-%m-%d')

    # Pega o nome do mês e ano atual
    month_folder = os.path.join(root, f'{today.month:02d}-{today.year}')

    # Cria pasta do mês caso não exista
    if not os.path.exists(month_folder):
        os.makedirs(month_folder)

    # Pega dia atual
    day_folder = os.path.join(month_folder, str(today.day))

    # Cria pasta do dia caso não exista
    if not os.path.exists(day_folder):
        os.makedirs(day_folder)

    # Seta arquivo de saída e headers do backup
    filename = os.path.join(day_folder, 'history.csv')
    header = ['nfe', 'date', 'supplier', 'value']

    # Realiza consulta na tabela 'history'
    query = database.read(
        table='history',
        fields=header
    )

    # Cria backup em um arquivo .csv
    write_csv(filename, header, query)

    # Repete o processo acima na tabela 'suppliers'
    filename = os.path.join(day_folder, 'suppliers.csv')
    header = ['supplier']

    query = database.read(
        table='suppliers',
        fields=header
    )

    write_csv(filename, header, query)

    # Cria namedtuple para guardar dados do backup mais antigo
    Oldest = namedtuple('OldestBackup', ['creation', 'fullname', 'parent'])

    oldest = Oldest(datetime.now(), '', '')
    backups_count = 0

    # Itera sobra todos os arquivos na pasta de backups
    for month_folder in os.listdir(root):
        month_fullname = os.path.join(root, month_folder)

        # Caso não seja uma pasta, retorna
        if not os.path.isdir(month_fullname):
            continue

        # Itera sobre cada pasta de backup na pasta do mês
        for day_folder in os.listdir(month_fullname):
            day_fullname = os.path.join(month_fullname, day_folder)
            creation_time = datetime.fromtimestamp(os.path.getctime(day_fullname))
            backups_count += 1

            # Se a data de criação for menor que a data mais antiga atual, substitui
            if creation_time < oldest.creation:
                oldest = Oldest(creation_time, day_fullname, month_fullname)

    # Caso a quantidade de backups seja maior que a configuração 'max_backups' remove o backup mais antigo
    if backups_count > int(max_backups):
        shutil.rmtree(oldest.fullname)

        # Caso a pasta do mês esteja vazia então remove-a
        if len(os.listdir(oldest.parent)) == 0:
            os.removedirs(oldest.parent)

    # Salva data do último backup
    with open(backup_config_path, 'w', encoding='utf8') as f:
        f.write(json.dumps({"last_backup": last_backup}, indent=4))
