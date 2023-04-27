"""Conexão e manipulação do banco de dados."""

import os
from enum import Enum
from datetime import datetime

from PySide6.QtSql import QSqlDatabase, QSqlQuery

from utils import get_config, ConfigSection


class QueryError(Exception):
    """Exceção lançada ao falhar uma query."""

    def __init__(self, query: str):
        self.query = query


class DatabaseState(Enum):
    """Estados de conexão com o banco de dados."""
    CONNECTED = 1
    NO_DATABASE = 2
    DATABASE_NOT_FOUND = 3


class DatabaseConnection:
    """Classe responsável por manter a conexão com o banco de dados."""
    State: DatabaseState = DatabaseState

    def __init__(self):
        self._connection: QSqlDatabase | None = None
        self.connection_state: DatabaseState = DatabaseState.NO_DATABASE
        self.location = ''

    @property
    def connection(self):
        return self._connection

    def connect(self):
        """Tenta se conectar ao banco de dados."""
        config = get_config(ConfigSection.DATABASE)
        db = config['name']

        # Verifica se o banco de dados pode ser localizado
        if not self.check_location(db):
            self._connection = None
            return

        self.location = db

        self._connection = QSqlDatabase.addDatabase('QSQLITE')
        self._connection.setDatabaseName(db)

        if self._connection.open():
            self.connection_state = DatabaseState.CONNECTED

            self.create_tables()

    def disconnect(self):
        """Desconecta conexão caso esteja conectada"""
        if self._connection and self._connection.isOpen():
            self._connection.close()

    def check_location(self, path: str) -> bool:
        """Verifica se a localização do arquivo pode ser encontrada"""
        if not path:
            self.connection_state = DatabaseState.NO_DATABASE
            return False

        if not os.path.exists(path):
            self.connection_state = DatabaseState.DATABASE_NOT_FOUND
            return False

        return True

    # Cria tabelas caso não exista
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

    def create(self, table: str, fields: dict):
        """
        Cria registro em uma tabela.

        :param table: Nome da tabela
        :param fields: Campos no formato key: value
        """
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

    def read(self, table: str, fields: list[str], clause: str = '', values: list = None, distinct=False) -> QSqlQuery:
        """
        Lê registros em uma tabela e retorna o objeto com os resultados.

        :param table: Nome da tabela
        :param fields: Lista com o nome dos campos
        :param clause: Cláusula para filtrar, ordenar ou agrupar
        :param values: Lista de valores para substituir placeholders
        :param distinct: Realizar a query com registros únicos ou não
        :return: Objeto contendo a query em questão
        """
        query = QSqlQuery(self._connection)

        query.prepare(
            f"""
            SELECT {'DISTINCT' if distinct else ''} {', '.join(fields)} FROM {table}
            {clause}
            """
        )

        if values:
            for value in values:
                query.addBindValue(value)

        if not query.exec():
            raise QueryError(f'Failed execution on query expression: {query.lastQuery()}')

        return query

    def update(self, table: str, fields: dict, clause: str, force=False):
        """
        Atualiza registros em uma tabela.

        :param table: Nome da tabela
        :param fields: Campos no formato key: value
        :param clause: Cláusula para filtrar
        :param force: Forçar update sem clause
        """
        if 'WHERE' not in clause and not force:
            raise QueryError(f'Update statement without WHERE clause')

        query = QSqlQuery(self._connection)

        query.prepare(
            f"""
            UPDATE {table} 
            SET {', '.join([field + '=?' for field in fields.keys()])}
            {clause}
            """
        )

        for value in fields.values():
            query.addBindValue(value)

        if not query.exec():
            raise QueryError(f'Failed execution on query expression: {query.lastQuery()}')

    def delete(self, table: str, clause: str, force=False):
        """
        Deleta registros em uma tabela.

        :param table: Nome da tabela
        :param clause: Cláusula para filtrar
        :param force: Forçar delete sem clause
        :return:
        """
        if 'WHERE' not in clause and not force:
            raise QueryError(f'Delete statement without WHERE clause')

        query = QSqlQuery(self._connection)

        query.prepare(
            f"""
            DELETE FROM {table}  
            {clause}
            """
        )

        if not query.exec():
            raise QueryError(f'Failed execution on query expression: {query.lastQuery()}')

    def is_unique(self, table: str, field: str, key: str) -> bool:
        """
        Retorna se o registro enviado é único na tabela.

        :param table: Nome da tabela
        :param field: Nome do campo
        :param key: Valor do campo
        :return: True se o valor for único, do contrário False
        """
        query = QSqlQuery(self._connection)

        query.prepare(
            f"""
            SELECT COUNT(*) FROM {table}
            WHERE {field} LIKE ?
            """
        )

        query.addBindValue(key)

        if not query.exec():
            raise QueryError(f'Failed execution on query expression: {query.lastQuery()}')

        query.first()

        return not bool(query.value(0))

    def reset_sequence(self, table: str):
        """
        Reseta o histórico da primary key da tabela enviada.

        :param table: Nome da tabela
        """
        query = QSqlQuery(self._connection)

        query.prepare(
            """
            DELETE FROM sqlite_sequence 
            WHERE name LIKE ?
            """
        )

        query.addBindValue(table)

        if not query.exec():
            raise QueryError(f'Failed execution on query expression: {query.lastQuery()}')

    def delete_year(self, year: str):
        """
        Deleta todos os registros de um ano específico.

        :param year:
        """
        query = QSqlQuery(self._connection)
        query.exec(f"DELETE FROM history WHERE strftime('%Y', date) LIKE {year}")

    def get_years(self, force_current_year: bool = True) -> list[str]:
        """
        Retorna anos dos dados.

        :param force_current_year:
        :return: Lista de anos
        """
        query = QSqlQuery(self._connection)
        query.exec("SELECT DISTINCT strftime('%Y', date) FROM history ORDER BY date")

        years = []

        while query.next():
            years.append(query.value(0))

        if not years and force_current_year:
            current_year = str(datetime.today().year)
            years.append(current_year)

        return years
