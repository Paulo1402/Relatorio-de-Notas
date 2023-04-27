"""Funções de configurações."""

import json
import os

from . import APPDATA_DIR, ConfigSection


def get_config(section: ConfigSection = ConfigSection.ALL) -> dict:
    """
    Retorna configurações do aplicativo.

    :param section: Sessão desejada
    :return: Dicionário com as configurações
    """
    path = os.path.join(APPDATA_DIR, 'config.json')

    # Caso o arquivo não exista ou não possa ser validado, cria um arquivo novo
    try:
        with open(path, 'r', encoding='utf8') as f:
            config = json.loads(f.read())

            # Tenta validar o arquivo, caso não consiga, força o tratamento
            app = config['app']
            database = config['database']

            _ = app['theme']

            _ = database['name']
            _ = database['backup_frequency']
            _ = database['max_backups']
    except (FileNotFoundError, KeyError, ValueError, json.JSONDecodeError):
        config = {
            'app': {
                'theme': 'dark',
            },
            'database': {
                'name': '',
                'backup_frequency': 'weekly',
                'max_backups': 5
            }
        }

        set_config(config)

    # Retorna objeto de configuração de acordo com a sessão requerida
    if section == ConfigSection.APP:
        return config['app']
    elif section == ConfigSection.DATABASE:
        return config['database']

    return config


def set_config(config: dict, section: ConfigSection = ConfigSection.ALL):
    """
    Seta configurações do aplicativo

    :param config: Dados para salvar
    :param section: Sessão enviada
    """

    # Retorna objeto de config completo caso se esteja setando apenas uma sessão
    if section != ConfigSection.ALL:
        old_config = get_config()

        section_name = 'app' if section == ConfigSection.APP else 'database'
        old_config[section_name] = config

        config = old_config

    path = os.path.join(APPDATA_DIR, 'config.json')
    print('set config', config)

    with open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(config, indent=4))
