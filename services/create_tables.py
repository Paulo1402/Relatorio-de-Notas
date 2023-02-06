from PyQt6.QtSql import QSqlQuery

from database.connection import connection

create_table_query = QSqlQuery(connection)

create_table_query.exec("DROP TABLE IF EXISTS history")
create_table_query.exec("DROP TABLE IF EXISTS suppliers")

create_table_query.exec(
    """
    CREATE TABLE history (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        nfe INTEGER NOT NULL,
        date TEXT NOT NULL,
        supplier TEXT NOT NULL,
        value REAL NOT NULL
    )
    """
)

create_table_query.exec(
    """
    CREATE TABLE suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        supplier TEXT NOT NULL
    )
    """
)
