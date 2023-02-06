import csv

from PyQt6.QtSql import QSqlQuery

from database.connection import connection
from utils import parse_date, from_currency_to_float

QSqlQuery(connection).exec('DELETE FROM history')
QSqlQuery(connection).exec('DELETE FROM suppliers')

populate_table_query = QSqlQuery(connection)

populate_table_query.prepare(
    """
    INSERT INTO history (
        nfe,
        date,
        supplier,
        value    
    )
    VALUES (?, ?, ?, ?)
    """
)

with open('../history.csv') as f:
    csvreader = csv.reader(f, delimiter=';')
    header = True

    for _, nfe, date, supplier, value in csvreader:
        if not header:
            populate_table_query.addBindValue(nfe)
            populate_table_query.addBindValue(parse_date(date, '%d/%m/%Y', '%Y-%m-%d'))
            populate_table_query.addBindValue(supplier)
            populate_table_query.addBindValue(from_currency_to_float(value))

            populate_table_query.exec()

        header = False

query = QSqlQuery(connection)
query.exec("SELECT count(*) FROM history")
query.first()

print(query.value(0))

populate_table_query.prepare(
    """
    INSERT INTO suppliers (
        supplier
    )
    VALUES (?)
    """
)

with open('../suppliers.csv') as f:
    csvreader = csv.reader(f, delimiter=';')
    header = True

    for supplier in csvreader:

        if not header:
            populate_table_query.addBindValue(supplier[0])

            populate_table_query.exec()

        header = False

query = QSqlQuery(connection)
query.exec("SELECT count(*) FROM suppliers")
query.first()

print(query.value(0))