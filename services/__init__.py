from datetime import datetime

from PyQt6.QtSql import QSqlQuery

from database.connection import connection
from services.crud import create, read, update, delete, QueryError

__all__ = [
    'QueryError',
    'create',
    'read',
    'update',
    'delete',
    'get_years',
    'close_connection'
]


# Retorna anos
def get_years():
    query = QSqlQuery(connection)
    query.exec("SELECT DISTINCT strftime('%Y', date) FROM history ORDER BY date")

    years = []

    while query.next():
        years.append(query.value(0))

    if not years:
        current_year = str(datetime.today().year)
        years.append(current_year)

    return years


def close_connection():
    connection.close()

# Retorna fornecedores
# def get_suppliers():
#     query = QSqlQuery(connection)
#     query.exec("SELECT DISTINCT supplier FROM history ORDER BY supplier")
#
#     suppliers = []
#
#     while query.next():
#         suppliers.append(query.value(0))
#
#     return suppliers
