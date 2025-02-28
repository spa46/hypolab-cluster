import requests
import sys
from .uuid_utils import generate_uuid, load_uuid, save_uuid

def register_device():
    device_uuid = load_uuid()
    if not device_uuid:
        device_uuid = generate_uuid()
        save_uuid(device_uuid)

    try:
        response = requests.post('http://abc.com/register', json={'uuid': device_uuid})
        if response.status_code == 200:
            print("Registration successful")
        else:
            print(f"Registration failed with status code: {response.status_code}")
            sys.exit(1)
    except requests.RequestException as e:
        print(f"Registration failed with exception: {e}")
        sys.exit(1)