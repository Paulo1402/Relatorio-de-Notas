from PyQt6.QtSql import QSqlQuery

from database.connection import connection

create_table_query = QSqlQuery(connection)

create_table_query.exec(
    """
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        nfe TEXT NOT NULL,
        date TEXT NOT NULL,
        supplier TEXT NOT NULL,
        value TEXT NOT NULL
    )
    """
)

create_table_query.exec(
    """
    CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        supplier TEXT NOT NULL
    )
    """
)
