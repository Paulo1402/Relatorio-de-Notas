import json
import os

# Caminho relativo ao main.py
BASEDIR = os.path.dirname(os.path.dirname(__file__))


# Retorna configurações do aplicativo
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
        config = {
            'database': None,
            'backup': {
                'frequency': 'weekly',
                'max_backups': 5
            }
        }

        set_config(config)

    return config


# Seta configurações do aplicativo
def set_config(config: dict):
    path = os.path.join(BASEDIR, 'config.json')

    with open(path, 'w'):
        pass

    with open(os.open(path, os.O_RDWR), 'w', encoding='utf8') as f:
        f.write(json.dumps(config, indent=4))
