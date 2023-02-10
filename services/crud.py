from PyQt6.QtSql import QSqlQuery

from database.connection import connection


# Exceção lançada ao falhar uma query
class QueryError(Exception):
    def __init__(self, query):
        self.query = query


# Cria registro no banco de dados
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


# Lê registros de uma tabela e retorna o objeto com os resultados
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


# Atualiza registros no banco de dados
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


# Deleta registros em uma tabela
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
