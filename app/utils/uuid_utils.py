import uuid
import os
import json

CONFIG_FILE = 'config.json'

def generate_uuid():
    return str(uuid.uuid4())

def load_uuid():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get('uuid')
    return None

def save_uuid(uuid):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'uuid': uuid}, f)