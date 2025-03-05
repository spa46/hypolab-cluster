import os
import sys
import time
import logging
import re


logger = logging.getLogger('app')


def create_lock_file(lock_file):
    with open(lock_file, 'w') as f:
        pass


def restart_server():
    os.environ['FLASK_APP'] = 'app:create_app'
    for i in range(5, 0, -1):
        print(f"Server restarting in {i} seconds...")
        time.sleep(1)

    print()
    os.execv(sys.executable, [sys.executable] + sys.argv)


def save_to_dotenv(key, value):
    dotenv_path = '.env'
    key_value_pattern = re.compile(rf'^{key}=.*$', re.MULTILINE)

    with open(dotenv_path, 'r') as f:
        content = f.read()

    if re.search(key_value_pattern, content):
        content = re.sub(key_value_pattern, f'{key}={value}', content)
    else:
        content += f'{key}={value}\n'

    with open(dotenv_path, 'w') as f:
        f.write(content)