import csv

from PySide6.QtSql import QSqlQuery

from src.services import DatabaseConnection
from src.utils import parse_date, from_currency_to_float

if __name__ == '__main__':
    database = DatabaseConnection()
    database.connect()

    connection = database.connection

    # Deleta conteúdo das tabelas
    QSqlQuery(connection).exec('DELETE FROM history')
    QSqlQuery(connection).exec('DELETE FROM suppliers')

    # Cria objeto com a conexão
    populate_table_query = QSqlQuery(connection)

    # Insere dados na tabela (USADO COMO SEED DURANTE O DESENVOLVIMENTO)
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

    # Faz a modelagem dos dados de um arquivo .csv para inserir na tabela
    with open('history.csv', 'r', encoding='latin') as f:
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

    # Verifica se a inserção foi feita corretamente
    query = QSqlQuery(connection)
    query.exec("SELECT count(*) FROM history")
    query.first()
    print(query.value(0))

    # Repete o mesmo procedimento na tabela abaixo
    populate_table_query.prepare(
        """
        INSERT INTO suppliers (
            supplier
        )
        VALUES (?)
        """
    )

    with open('suppliers.csv', 'r', encoding='latin') as f:
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
