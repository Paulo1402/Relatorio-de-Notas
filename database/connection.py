import os

from PyQt6.QtSql import QSqlDatabase

DB = os.path.join(os.path.dirname(__file__), 'db.sqlite')

if not os.path.exists(DB):
    with open(DB, 'w'):
        pass

connection = QSqlDatabase.addDatabase('QSQLITE')
connection.setDatabaseName(DB)

if not connection.open():
    raise ConnectionError('Could not connect to database')
