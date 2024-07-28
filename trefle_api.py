import requests
from timestamp_handler import load_timestamps, should_update, update_timestamp

API_KEY = 'wH6iPDs7cs8qJfQBs7pqxXe_g6Afg-3i8SsKQ2rzW80'
timestamps = load_timestamps()

BASE_URL = 'https://trefle.io/api/v1/plants/{}?token={}';
GENUS_URL = 'https://trefle.io/api/v1/genus/{}?token={}';
FAMILY_URL = 'https://trefle.io/api/v1/families/{}?token={}';

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('data')
    except requests.exceptions.RequestException as e:
        print("Error fetching data from url '{}': {}".format(url, e))
        return None

def get_plant_info(plant_id):
    url = BASE_URL.format(plant_id, API_KEY)
    return fetch_data(url)

def fetch_species_taxonomy(starting_id):
    plant_info = get_plant_info(starting_id)
    if not plant_info:
        return

    current_info = get_plant_info(starting_id)
    genus_id = current_info.get('genus_id')

    species_name = current_info.get('scientific_name')
    species_id = current_info.get('id')
    image_url = current_info.get('image_url', 'No image available')
    observations = current_info.get('observations', 'No observations available')
    species_taxonomy = {
        "species_id": species_id,
        "genus_id": genus_id,
        "family_id": None,
        "division_order_id": None,
        "division_class_id": None,
        "division_id": None,
        "subkingdom_id": None,
        "kingdom_id": None,
        "species": species_name,
        "genus": None,
        "family": None,
        "division_order": None,
        "division_class": None,
        "division": None,
        "subkingdom": None,
        "kingdom": None,
        "image_url": image_url,
        "observations": observations
    }

    def fetch_and_add_taxonomy(endpoint_id, url_template, level_name, taxonomy_dict):
        if endpoint_id:
            url = url_template.format(endpoint_id, API_KEY)
            info = fetch_data(url)
            if info:
                taxonomy_dict[level_name + "_id"] = info.get('id')
                taxonomy_dict[level_name] = info.get('name', 'Unknown')
                return info
        return None

    genus_info = fetch_and_add_taxonomy(genus_id, GENUS_URL, 'genus', species_taxonomy)
    if not genus_info:
        return species_taxonomy

    family_id = genus_info.get('family', {}).get('id')
    family_info = fetch_and_add_taxonomy(family_id, FAMILY_URL, 'family', species_taxonomy)
    if not family_info:
        return species_taxonomy

    species_taxonomy.update({
        "division_order_id": family_info.get('division_order', {}).get('id'),
        "division_class_id": family_info.get('division_order', {}).get('division_class', {}).get('id'),
        "division_id": family_info.get('division_order', {}).get('division_class', {}).get('division', {}).get('id'),
        "subkingdom_id": family_info.get('division_order', {}).get('division_class', {}).get('division', {}).get('subkingdom', {}).get('id'),
        "kingdom_id": family_info.get('division_order', {}).get('division_class', {}).get('division', {}).get('subkingdom', {}).get('kingdom', {}).get('id'),
        "division_order": family_info.get('division_order', {}).get('name', 'Unknown'),
        "division_class": family_info.get('division_order', {}).get('division_class', {}).get('name', 'Unknown'),
        "division": family_info.get('division_order', {}).get('division_class', {}).get('division', {}).get('name', 'Unknown'),
        "subkingdom": family_info.get('division_order', {}).get('division_class', {}).get('division', {}).get('subkingdom', {}).get('name', 'Unknown'),
        "kingdom": family_info.get('division_order', {}).get('division_class', {}).get('division', {}).get('subkingdom', {}).get('kingdom', {}).get('name', 'Unknown')
    })

    return species_taxonomy
