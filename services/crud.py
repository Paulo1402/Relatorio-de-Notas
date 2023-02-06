from PyQt6.QtSql import QSqlQuery

from database.connection import connection


class QueryError(Exception):
    def __init__(self, query):
        self.query = query


def create(table: str, fields: dict):
    query = QSqlQuery(connection)

    query.prepare(
        f"""
        INSERT INTO {table} ({', '.join([field for field in fields.keys()])})
        VALUES ({', '.join(['?' for _ in fields])})
        """
    )

    for value in fields.values():
        query.addBindValue(value)

    if not query.exec():
        raise QueryError(f'Failed execution on query expression: {query.lastQuery()}')


def read(table: str, fields: list[str], where: dict):
    query = QSqlQuery(connection)

    clause: str = where['clause']
    values: list = where['values']

    query.prepare(
        f"""
        SELECT {', '.join(fields)} FROM {table}
        {clause}
        """
    )

    for value in values:
        query.addBindValue(value)

    if not query.exec():
        raise QueryError(f'Failed execution on query expression: {query.lastQuery()}')

    return query


def update(table: str, fields: dict, id_record: int):
    query = QSqlQuery(connection)

    query.prepare(
        f"""
        UPDATE {table} 
        SET {', '.join([field + '=?' for field in fields.keys()])}
        WHERE id LIKE {id_record}
        """
    )

    for value in fields.values():
        query.addBindValue(value)

    if not query.exec():
        raise QueryError(f'Failed execution on query expression: {query.lastQuery()}')


def delete(table: str, id_record: int):
    query = QSqlQuery(connection)

    query.prepare(
        f"""
        DELETE FROM {table}  
        WHERE id LIKE {id_record}
        """
    )

    if not query.exec():
        raise QueryError(f'Failed execution on query expression: {query.lastQuery()}')

# create('history', {
#     'nfe': '1414',
#     'date': '2023-01-20',
#     'supplier': 'TEST',
#     'value': '1400'
# })

# q = read('history', ['nfe'], {
#     'clause': 'id > 0',
#     'values': []
# })
#
# q.first()
#
# while q.next():
#     print(q.value(0))

# update('history', {
#     'nfe': '1420',
#     'date': '2023-01-31',
#     'supplier': 'TEST edit',
#     'value': '1800'
# }, id_record=528)

# delete('history', id_record=528)
