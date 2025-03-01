import uuid
import os
import yaml

def generate_uuid():
    return str(uuid.uuid4())

def load_uuid(config_file):
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
            return config.get('uuid')
    return None

def save_uuid(uuid, config_file):
    with open(config_file, 'w') as f:
        yaml.dump({'uuid': uuid}, f)