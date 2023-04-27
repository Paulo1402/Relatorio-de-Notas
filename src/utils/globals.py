"""Constantes usadas ao longo do programa."""
import os
from pathlib import Path

APP_NAME = 'Relatório de Notas'

# Caminho relativo ao main.py (.exe quando compilado)
BASEDIR = Path(__file__).parent.parent

# Caminho para criar e manipular arquivos auxiliares (log, config)
APPDATA_DIR = BASEDIR

# Diretórios Windows com restrição de escrita
windows_installation_paths = [
    os.getenv('ProgramFiles(x86)'),
    os.getenv('ProgramW6432')
]

# Caso o app for instalado em um dos diretórios com restrições de escrita no Windows altera o diretório
# para criar arquivos auxiliares.
for path in windows_installation_paths:
    if BASEDIR.is_relative_to(path):
        APPDATA_DIR = os.path.join(os.getenv('APPDATA'), APP_NAME)

        if not os.path.exists(APPDATA_DIR):
            os.mkdir(APPDATA_DIR)

        break

# Desativa warnings
DEBUG = False

# Cores dos temas
DARK_COLOR = '#f4d1ae'
LIGHT_COLOR = '#346685'

# Tabelas e campos da tabela
TABLES = {
    'history': ['nfe', 'date', 'supplier', 'value'],
    'suppliers': ['supplier'],
}

# Tabelas com primary keys automáticas
AUTO_INCREMENTED_TABLES = ['suppliers']
