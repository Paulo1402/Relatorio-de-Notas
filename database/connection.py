import os

from PyQt6.QtSql import QSqlDatabase, QSqlQuery

# Caminho para o banco de dados
DB = os.path.join(os.path.dirname(__file__), 'db.sqlite')

# Cria conexão com banco de dados
connection = QSqlDatabase.addDatabase('QSQLITE')
connection.setDatabaseName(DB)

# Abre conexão com banco de dados
if not connection.open():
    raise ConnectionError('Could not connect to database')

# Cria objeto de conexão
create_table_query = QSqlQuery(connection)

# Cria tabela suppliers caso não exista
create_table_query.exec(
    """
    CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        supplier TEXT NOT NULL
    )
    """
)

# Cria tabela history caso não exista
create_table_query.exec(
    """
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        nfe INTEGER NOT NULL,
        date TEXT NOT NULL,
        supplier TEXT NOT NULL,
        value REAL NOT NULL
    )
    """
)
