import requests
import time
import json
import random
import sys
import os
from datetime import datetime, timedelta

def get_client_ids(client_ids_file):
    """ Load client IDs from the file, or return empty doc """
    if os.path.exists(client_ids_file):
        with open(client_ids_file, 'r') as file:
            return json.load(file)
    return {}

def save_client_id(client_ids_file, client_id, details):
    """ Save a new client ID with details to the file. """
    client_ids = get_client_ids(client_ids_file)
    client_ids[client_id] = details
    with open(client_ids_file, 'w') as file:
        json.dump(client_ids, file)

def generate_client_id(client_ids_file, client_ids):
        part1 = random.randint(100000000, 999999999)
        part2 = int(time.time())
        new_client_id = f'{part1}.{part2}'
        save_client_id(client_ids_file, new_client_id, {'User type': 'New'})  # Add details as needed
        return new_client_id