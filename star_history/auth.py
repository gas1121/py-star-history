import json
import os


def get_auth_data():
    auth_file_path = os.path.join(os.path.dirname(__file__), 'auth.json')
    with open(auth_file_path) as auth_file:
        auth_data = json.load(auth_file)
    return auth_data
