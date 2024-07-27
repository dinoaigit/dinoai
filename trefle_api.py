import requests
from timestamp_handler import load_timestamps, should_update, update_timestamp

API_KEY = 'wH6iPDs7cs8qJfQBs7pqxXe_g6Afg-3i8SsKQ2rzW80'
timestamps = load_timestamps()


def get_kingdoms():
    try:
        if should_update(timestamps, "kingdoms"):
            url = f'https://trefle.io/api/v1/kingdoms?token={API_KEY}'
            response = requests.get(url)
            response.raise_for_status()  # HTTPError durumunda istisna fırlatır
            update_timestamp(timestamps, "kingdoms")
            data = response.json()['data']
            print("Kingdoms:", data)
            return data
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching kingdoms: {e}")
        return []


def get_subkingdoms(kingdom_id):
    try:
        if should_update(timestamps, "subkingdoms", kingdom_id):
            url = f'https://trefle.io/api/v1/kingdoms/{kingdom_id}/subkingdoms?token={API_KEY}'
            response = requests.get(url)
            response.raise_for_status()
            update_timestamp(timestamps, "subkingdoms", kingdom_id)
            data = response.json()['data']
            print(f"Subkingdoms for kingdom_id {kingdom_id}:", data)
            return data
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching subkingdoms for kingdom_id {kingdom_id}: {e}")
        return []


def get_divisions(subkingdom_id):
    try:
        if should_update(timestamps, "divisions", subkingdom_id):
            url = f'https://trefle.io/api/v1/subkingdoms/{subkingdom_id}/divisions?token={API_KEY}'
            response = requests.get(url)
            response.raise_for_status()
            update_timestamp(timestamps, "divisions", subkingdom_id)
            data = response.json()['data']
            print(f"Divisions for subkingdom_id {subkingdom_id}:", data)
            return data
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching divisions for subkingdom_id {subkingdom_id}: {e}")
        return []


def get_classes(division_id):
    try:
        if should_update(timestamps, "classes", division_id):
            url = f'https://trefle.io/api/v1/divisions/{division_id}/classes?token={API_KEY}'
            response = requests.get(url)
            response.raise_for_status()
            update_timestamp(timestamps, "classes", division_id)
            data = response.json()['data']
            print(f"Classes for division_id {division_id}:", data)
            return data
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching classes for division_id {division_id}: {e}")
        return []


def get_orders(class_id):
    try:
        if should_update(timestamps, "orders", class_id):
            url = f'https://trefle.io/api/v1/classes/{class_id}/orders?token={API_KEY}'
            response = requests.get(url)
            response.raise_for_status()
            update_timestamp(timestamps, "orders", class_id)
            data = response.json()['data']
            print(f"Orders for class_id {class_id}:", data)
            return data
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching orders for class_id {class_id}: {e}")
        return []


def get_families(order_id):
    try:
        if should_update(timestamps, "families", order_id):
            url = f'https://trefle.io/api/v1/orders/{order_id}/families?token={API_KEY}'
            response = requests.get(url)
            response.raise_for_status()
            update_timestamp(timestamps, "families", order_id)
            data = response.json()['data']
            print(f"Families for order_id {order_id}:", data)
            return data
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching families for order_id {order_id}: {e}")
        return []


def get_genuses(family_id):
    try:
        if should_update(timestamps, "genuses", family_id):
            url = f'https://trefle.io/api/v1/families/{family_id}/genuses?token={API_KEY}'
            response = requests.get(url)
            response.raise_for_status()
            update_timestamp(timestamps, "genuses", family_id)
            data = response.json()['data']
            print(f"Genuses for family_id {family_id}:", data)
            return data
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching genuses for family_id {family_id}: {e}")
        return []


def get_species(genus_id):
    try:
        if should_update(timestamps, "species", genus_id):
            url = f'https://trefle.io/api/v1/genuses/{genus_id}/species?token={API_KEY}'
            response = requests.get(url)
            response.raise_for_status()
            update_timestamp(timestamps, "species", genus_id)
            data = response.json()['data']
            print(f"Species for genus_id {genus_id}:", data)
            return data
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching species for genus_id {genus_id}: {e}")
        return []
