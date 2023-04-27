"""Workers para trabalhar em outras threads."""

import csv
import functools
import itertools
import json
import os
import shutil
from datetime import datetime

from PySide6.QtCore import QThread, Signal
from PySide6.QtSql import QSqlQuery

from utils import TABLES, AUTO_INCREMENTED_TABLES, Logger, get_config, ConfigSection, OldestBackup
from . import DatabaseConnection, QueryError


class DoBackupWorker(QThread):
    """Worker para realizar o backup."""

    progress = Signal(int)

    def __init__(self, database: DatabaseConnection):
        super().__init__()

        self.database = database

    @staticmethod
    def _write_csv(filename: str, header: list, query: QSqlQuery):
        """
        Cria arquivo csv com dados da tabela.

        :param filename: Diretório de saída do arquivo
        :param header: Cabeçalhos da tabela
        :param query: Query com dados da tabela
        """
        with open(filename, 'w', encoding='latin') as f:
            writer = csv.writer(f, delimiter=';', quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
            writer.writerow(header)

            while query.next():
                values = [query.value(i) if not query.isNull(i) else None for i in range(len(header))]
                writer.writerow(values)

    def run(self):
        """Executa tarefa do Worker."""

        # Pega as configurações do aplicativo
        config = get_config(ConfigSection.DATABASE)

        db = config['name']
        frequency = config['backup_frequency']
        max_backups = config['max_backups']

        # Caso não haja um banco de dados configurado ou 'no_backups' está setado, aborta backup
        if not db or frequency == 'no_backups':
            return

        # Pega raiz da pasta de backups
        root = os.path.join(os.path.dirname(db), 'backups')

        # Cria raiz caso não exista
        if not os.path.exists(root):
            os.makedirs(root)

        # Pega o arquivo de configuração da pasta de backup
        backup_config_path = os.path.join(root, 'config.json')

        # Tenta coletar data do último backup e transforma em um objeto datetime
        try:
            with open(backup_config_path, 'r', encoding='utf8') as f:
                config = json.loads(f.read())

                last_backup = config['last_backup']
                last_backup = datetime.strptime(last_backup, '%Y-%m-%d').date()
        except (FileNotFoundError, KeyError, ValueError, json.JSONDecodeError):
            last_backup = None

        # Retorna data atual
        today = datetime.today().date()

        # Verifica se há necessidade de realizar o backup com base na configuração 'frequency'
        if last_backup:
            if frequency == 'diary' and last_backup == today:
                return
            elif frequency == 'weekly' and last_backup.isocalendar().week == today.isocalendar().week:
                return
            elif frequency == 'monthly' and last_backup.month == today.month:
                return

        # Transforma datetime em string novamente
        last_backup = today.strftime('%Y-%m-%d')

        # Pega o nome do mês e ano atual
        month_folder = os.path.join(root, f'{today.month:02d}-{today.year}')

        # Cria pasta do mês caso não exista
        if not os.path.exists(month_folder):
            os.makedirs(month_folder)

        # Pega dia atual
        day_folder = os.path.join(month_folder, str(today.day))

        # Cria pasta do dia caso não exista
        if not os.path.exists(day_folder):
            os.makedirs(day_folder)

        # Tabelas e seus campos
        count = 0

        for table, header in TABLES.items():
            count += 1

            # Seta arquivo de saída
            filename = os.path.join(day_folder, f'{table}.csv')

            # Realiza consulta
            query = self.database.read(
                table=table,
                fields=header
            )

            # Cria backup em um arquivo .csv
            self._write_csv(filename, header, query)

            progress = int((count / len(TABLES)) * 100)
            self.progress.emit(progress)

        # Cria namedtuple para guardar dados do backup mais antigo
        oldest = OldestBackup(creation=datetime.now(), fullname='', parent='')
        backups_count = 0

        # Itera sobra todos os arquivos na pasta de backups
        for month_folder in os.listdir(root):
            month_fullname = os.path.join(root, month_folder)

            # Caso não seja uma pasta, pula a iteração
            if not os.path.isdir(month_fullname):
                continue

            # Itera sobre cada pasta de backup na pasta do mês
            for day_folder in os.listdir(month_fullname):
                day_fullname = os.path.join(month_fullname, day_folder)
                creation_time = datetime.fromtimestamp(os.path.getctime(day_fullname))
                backups_count += 1

                # Se a data de criação for menor que a data mais antiga atual, substitui
                if creation_time < oldest.creation:
                    oldest = OldestBackup(creation=creation_time, fullname=day_fullname, parent=month_fullname)

        # Caso a quantidade de backups seja maior que a configuração 'max_backups' remove o backup mais antigo
        if backups_count > int(max_backups):
            shutil.rmtree(oldest.fullname)

            # Caso a pasta do mês esteja vazia então remove-a
            if len(os.listdir(oldest.parent)) == 0:
                os.removedirs(oldest.parent)

        # Salva data do último backup
        with open(backup_config_path, 'w', encoding='utf8') as f:
            f.write(json.dumps({"last_backup": last_backup}, indent=4))


class ImportBackupWorker(QThread):
    """Worker para importar backup."""

    # Signals
    progress = Signal(int, str)
    error = Signal(str)
    success = Signal()

    def __init__(self, database: DatabaseConnection, source: str):
        super().__init__()

        self.database = database
        self.source = source

    def run(self):
        """Executa tarefa do Worker."""
        expected_files = [f'{t}.csv' for t in TABLES.keys()]
        files = [f for f in os.listdir(self.source) if f in expected_files]

        # Verifica se todas as tabelas estão no diretório enviado
        if len(files) != len(expected_files):
            message = 'Não foram encontrados um ou mais arquivos dentro do diretório especificado.\n' \
                      f'Os arquivos esperados são: {", ".join(expected_files)}'
            self.error.emit(message)
            return

        file_count = 0

        # É necessário usar a variável 'expected_files' porque precisamos inserir os dados na ordem correta das
        # tabelas. Usando a lista retornada em 'files' é possível que alguma tabela esteja fora de ordem.
        for file in expected_files:
            # Pega nome da tabela
            table = file.replace('.csv', '')
            file_count += 1

            # Recupera dados do backup
            with open(os.path.join(self.source, file), 'r', encoding='latin') as f:
                # Cria generator original
                _reader = csv.reader(f, delimiter=';')

                # Pega o cabeçalho
                header = next(_reader)

                # Cria cópias a partir do generator original
                reader_rows, reader_total_rows = itertools.tee(_reader, 2)

                # Verifica se os campos do arquivo de backup coincidem com os campos das tabelas
                for field in header:
                    if field not in TABLES[table]:
                        message = f'Os campos do arquivo de backup "{file}" não coincidem com os campos esperados ' \
                                  f'para a tabela "{table}".\n' \
                                  f'Apenas importe arquivos gerados pelo próprio sistema de backup!'
                        self.error.emit(message)
                        return

                # Deleta dados atuais
                self.database.delete(table=table, clause='', force=True)

                # Zera sequência da primary key
                if table in AUTO_INCREMENTED_TABLES:
                    self.database.reset_sequence(table)

                # Pega total de linhas
                row_count = 1
                total_rows = functools.reduce(lambda count, _: count + 1, reader_total_rows, 0)

                # Insere dados na tabela
                try:
                    for row in reader_rows:
                        row_count += 1
                        parsed_row = [i if i else None for i in row]
                        fields = {field: value for field, value in list(zip(header, parsed_row))}

                        self.database.create(
                            table=table,
                            fields=fields
                        )

                        # Emite signal de progresso da tabela
                        progress = int((row_count / total_rows) * 100)
                        self.progress.emit(progress, table)

                except QueryError:
                    message = f'Não foi possível importar o arquivo de backup "{file}". ' \
                              f'Erro na linha: {row_count}.\n' \
                              'Apenas importe arquivos gerados pelo próprio sistema de backup! ' \
                              'Verifique o arquivo de backup e tente novamente.'

                    self.error.emit(message)

                    Logger().error(f'Failed to import backup on line {row_count} from "{file}".')
                    return

            # Emite signal de progresso principal
            progress = int((file_count / len(expected_files)) * 100)
            self.progress.emit(progress, 'main')

        self.success.emit()
