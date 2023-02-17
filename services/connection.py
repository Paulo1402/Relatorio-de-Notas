import os
from enum import Enum

from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from utils import get_config


# Exceção lançada ao falhar uma query
class QueryError(Exception):
    def __init__(self, query):
        self.query = query


class DatabaseState(Enum):
    CONNECTED = 1
    NO_DATABASE = 2
    DATABASE_NOT_FOUND = 3


class DatabaseConnection:
    STATE: DatabaseState = DatabaseState

    def __init__(self):
        self._connection: QSqlDatabase | None = None
        self._connection_state: DatabaseState = DatabaseState.NO_DATABASE

    @property
    def connection_state(self):
        return self._connection_state

    @property
    def connection(self):
        return self._connection

    def check_location(self, path):
        if not path:
            self._connection_state = DatabaseState.NO_DATABASE
        elif not os.path.exists(path):
            self._connection_state = DatabaseState.DATABASE_NOT_FOUND
        else:
            return True

    def connect(self):
        config = get_config()
        db = config['database']

        if not self.check_location(db):
            self._connection = None
            return

        self._connection = QSqlDatabase.addDatabase('QSQLITE')
        self._connection.setDatabaseName(db)

        if self._connection.open():
            self._connection_state = DatabaseState.CONNECTED

        self.create_tables()

    def disconnect(self):
        if self._connection:
            self._connection.close()

    # Cria tabelas
    def create_tables(self):
        query = QSqlQuery(self._connection)

        query.exec(
            """
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                supplier TEXT NOT NULL
            )
            """
        )

        query.exec(
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

    # Cria registro em uma tabela
    def create(self, table: str, fields: dict):
        query = QSqlQuery(self._connection)

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

        query.exec()

    # Lê registros em uma tabela e retorna o objeto com os resultados
    def read(self, table: str, fields: list[str], where: dict | None = None):
        query = QSqlQuery(self._connection)

        if not where:
            where = {
                "clause": '',
                "values": []
            }

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

    # Atualiza registros em uma tabela
    def update(self, table: str, fields: dict, id_record: int):
        query = QSqlQuery(self._connection)

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
    def delete(self, table: str, clause: str):
        query = QSqlQuery(self._connection)

        query.prepare(
            f"""
            DELETE FROM {table}  
            {clause}
            """
        )

        if not query.exec():
            raise QueryError(f'Failed execution on query expression: {query.lastQuery()}')
