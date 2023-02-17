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


# Retorna anos
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


def delete_year(database: DatabaseConnection, year: str):
    query = QSqlQuery(database.connection)
    query.exec(f"DELETE FROM history WHERE strftime('%Y', date) LIKE {year}")


def check_connection(func):
    def inner(self, *_, **__):
        if self.database.connection_state != DatabaseConnection.STATE.CONNECTED:
            QMessageBox.critical(self, 'CRÍTICO', 'Sem conexão com o banco de dados!')
            return

        func(self)

    return inner


def do_backup(database: DatabaseConnection):
    def write_csv(filename: str, header: list, query: QSqlQuery):
        with open(filename, 'w', encoding='utf8') as f:
            writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
            writer.writerow(header)

            while query.next():
                values = [query.value(i) for i in range(len(header))]
                writer.writerow(values)

    config = get_config()

    db = config['database']
    backup = config['backup']

    frequency = backup['frequency']
    max_backups = backup['max_backups']

    if frequency == 'no_backups' or not db:
        return

    root = os.path.join(os.path.dirname(db), 'backups')

    if not os.path.exists(root):
        os.makedirs(root)

    backup_config_path = os.path.join(root, 'config.json')

    try:
        with open(backup_config_path, 'r', encoding='utf8') as f:
            config = json.loads(f.read())

            last_backup = config['last_backup']
            last_backup = datetime.strptime(last_backup, '%Y-%m-%d')
    except (FileNotFoundError, KeyError, ValueError, json.JSONDecodeError):
        last_backup = None

    today = datetime.today().date()

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
        last_backup = today.strftime('%Y-%m-%d')

    month_folder = os.path.join(root, f'{today.month:02d}-{today.year}')

    if not os.path.exists(month_folder):
        os.makedirs(month_folder)

    day_folder = os.path.join(month_folder, str(today.day))

    if not os.path.exists(day_folder):
        os.makedirs(day_folder)

    filename = os.path.join(day_folder, 'history.csv')
    header = ['id', 'nfe', 'date', 'supplier', 'value']

    query = database.read(
        table='history',
        fields=header
    )

    write_csv(filename, header, query)

    filename = os.path.join(day_folder, 'suppliers.csv')
    header = ['id', 'supplier']

    query = database.read(
        table='suppliers',
        fields=header
    )

    write_csv(filename, header, query)

    backups = [folder for folder in os.listdir(root) if os.path.isdir(os.path.join(root, folder))]

    if len(backups) > int(max_backups):
        Oldest = namedtuple('OldestBackup', ['creation', 'fullname', 'parent'])
        oldest = Oldest(datetime.now(), '', '')

        for folder in backups:
            month_fullname = os.path.join(root, folder)

            for f in os.listdir(month_fullname):
                day_fullname = os.path.join(month_fullname, f)
                creation_time = datetime.fromtimestamp(os.path.getctime(day_fullname))

                if creation_time < oldest.creation:
                    oldest = Oldest(creation_time, day_fullname, month_fullname)

        shutil.rmtree(oldest.fullname)

        if len(os.listdir(oldest.parent)) == 0:
            os.removedirs(oldest.parent)

    with open(backup_config_path, 'w', encoding='utf8') as f:
        f.write(json.dumps({"last_backup": last_backup}, indent=4))
