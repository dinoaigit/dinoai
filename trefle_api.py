import requests

API_KEY = 'wH6iPDs7cs8qJfQBs7pqxXe_g6Afg-3i8SsKQ2rzW80'

def get_kingdoms():
    url = f'https://trefle.io/api/v1/kingdoms?token={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return []

def get_subkingdoms(kingdom_id):
    url = f'https://trefle.io/api/v1/kingdoms/{kingdom_id}/subkingdoms?token={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return []

def get_divisions(subkingdom_id):
    url = f'https://trefle.io/api/v1/subkingdoms/{subkingdom_id}/divisions?token={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return []

def get_classes(division_id):
    url = f'https://trefle.io/api/v1/divisions/{division_id}/classes?token={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return []

def get_orders(class_id):
    url = f'https://trefle.io/api/v1/classes/{class_id}/orders?token={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return []

def get_families(order_id):
    url = f'https://trefle.io/api/v1/orders/{order_id}/families?token={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return []

def get_genuses(family_id):
    url = f'https://trefle.io/api/v1/families/{family_id}/genuses?token={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return []

def get_species(genus_id):
    url = f'https://trefle.io/api/v1/genuses/{genus_id}/species?token={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return []
