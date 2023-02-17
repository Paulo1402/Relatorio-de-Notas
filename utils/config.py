import json
import os

# Caminho relativo ao main.py
BASEDIR = os.path.dirname(os.path.dirname(__file__))


def get_config():
    path = os.path.join(BASEDIR, 'config.json')

    try:
        with open(path, 'r', encoding='utf8') as f:
            config = json.loads(f.read())

            try:
                _ = config['database']
                backups = config['backup']

                _ = backups['frequency']
                _ = backups['max_backups']
            except (KeyError, ValueError):
                raise json.JSONDecodeError
    except (FileNotFoundError, json.JSONDecodeError):
        with open(path, 'w', encoding='utf8') as f:
            config = {
                'database': None,
                'backup': {
                    'frequency': 'weekly',
                    'max_backups': 5
                }
            }

            f.write(json.dumps(config, indent=4))

    return config


def set_config(config: dict):
    path = os.path.join(BASEDIR, 'config.json')

    with open(path, 'w', encoding='utf8') as f:
        f.write(json.dumps(config, indent=4))
