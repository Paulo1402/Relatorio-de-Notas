from PyQt6.QtSql import QSqlQuery

from database.connection import connection


class QueryError(Exception):
    pass


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


def read(table: str, fields: list[str], where: str):
    query = QSqlQuery(connection)

    query.prepare(
        f"""
        SELECT {', '.join(fields)} FROM {table}
        WHERE {' AND '.join(field for field in fields)}
        """
    )


def update(table: str, fields: dict, where: str):
    pass


def delete(table: str, where: str):
    pass
