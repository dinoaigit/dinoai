import requests
import time
from timestamp_handler import load_timestamps, should_update, update_timestamp

API_KEY = 'wH6iPDs7cs8qJfQBs7pqxXe_g6Afg-3i8SsKQ2rzW80'
timestamps = load_timestamps()

SPECIES_URL = 'https://trefle.io/api/v1/species/{}?token={}';
GENUS_URL = 'https://trefle.io/api/v1/genus/{}?token={}'
FAMILY_URL = 'https://trefle.io/api/v1/families/{}?token={}'

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('data')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from url '{url}': {e}")
        return None

def get_species_info(species_id):
    url = SPECIES_URL.format(species_id, API_KEY)
    return fetch_data(url)

def fetch_and_add_taxonomy(endpoint_id, url_template, level_name, taxonomy_dict):
    if endpoint_id:
        url = url_template.format(endpoint_id, API_KEY)
        info = fetch_data(url)
        if info:
            taxonomy_dict[level_name + "_id"] = info.get('id')
            taxonomy_dict[level_name] = info.get('name')
            time.sleep(0.5)  # Wait between API calls
            return info
    return None

def fetch_species_taxonomy(species_id):
    print(f"Fetching species taxonomy for species_id: {species_id}")
    
    species_info = get_species_info(species_id)
    if not species_info:
        print(f"Failed to fetch species info for species_id: {species_id}")
        return None

    genus_id = species_info.get('genus_id')
    species_name = species_info.get('scientific_name')
    image_url = species_info.get('image_url')
    observations = species_info.get('observations')
    
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

    # Fetch genus information and get family_id
    genus_info = fetch_and_add_taxonomy(genus_id, GENUS_URL, 'genus', species_taxonomy)
    if genus_info:
        family_info = genus_info.get('family', {})
        family_id = family_info.get('id')
        if family_id:
            species_taxonomy["family_id"] = family_id
            species_taxonomy["family"] = family_info.get('name')
            print(f"Family ID found: {family_id}")

            # Fetch family information and add other details
            family_info = fetch_and_add_taxonomy(family_id, FAMILY_URL, 'family', species_taxonomy)
            if family_info:
                species_taxonomy.update({
                    "division_order_id": family_info.get('division_order', {}).get('id') if family_info.get('division_order') else None,
                    "division_class_id": family_info.get('division_order', {}).get('division_class', {}).get('id') if family_info.get('division_order') and family_info.get('division_order').get('division_class') else None,
                    "division_id": family_info.get('division_order', {}).get('division_class', {}).get('division', {}).get('id') if family_info.get('division_order') and family_info.get('division_order').get('division_class') and family_info.get('division_order').get('division_class').get('division') else None,
                    "subkingdom_id": family_info.get('division_order', {}).get('division_class', {}).get('division', {}).get('subkingdom', {}).get('id') if family_info.get('division_order') and family_info.get('division_order').get('division_class') and family_info.get('division_order').get('division_class').get('division') and family_info.get('division_order').get('division_class').get('division').get('subkingdom') else None,
                    "kingdom_id": family_info.get('division_order', {}).get('division_class', {}).get('division', {}).get('subkingdom', {}).get('kingdom', {}).get('id') if family_info.get('division_order') and family_info.get('division_order').get('division_class') and family_info.get('division_order').get('division_class').get('division') and family_info.get('division_order').get('division_class').get('division').get('subkingdom') and family_info.get('division_order').get('division_class').get('division').get('subkingdom').get('kingdom') else None,
                    "division_order": family_info.get('division_order', {}).get('name') if family_info.get('division_order') else None,
                    "division_class": family_info.get('division_order', {}).get('division_class', {}).get('name') if family_info.get('division_order') and family_info.get('division_order').get('division_class') else None,
                    "division": family_info.get('division_order', {}).get('division_class', {}).get('division', {}).get('name') if family_info.get('division_order') and family_info.get('division_order').get('division_class') and family_info.get('division_order').get('division_class').get('division') else None,
                    "subkingdom": family_info.get('division_order', {}).get('division_class', {}).get('division', {}).get('subkingdom', {}).get('name') if family_info.get('division_order') and family_info.get('division_order').get('division_class') and family_info.get('division_order').get('division_class').get('division') and family_info.get('division_order').get('division_class').get('division').get('subkingdom') else None,
                    "kingdom": family_info.get('division_order', {}).get('division_class', {}).get('division', {}).get('subkingdom', {}).get('kingdom', {}).get('name') if family_info.get('division_order') and family_info.get('division_order').get('division_class') and family_info.get('division_order').get('division_class').get('division') and family_info.get('division_order').get('division_class').get('division').get('subkingdom') and family_info.get('division_order').get('division_class').get('division').get('subkingdom').get('kingdom') else None
                })
            else:
                print(f"Family information could not be fetched for family_id: {family_id}. Null values will be assigned.")
        else:
            print(f"Family ID not found for genus_id: {genus_id}. Null values will be assigned.")
    else:
        print(f"Genus information could not be fetched for genus_id: {genus_id}. Null values will be assigned.")

    print(f"Species taxonomy fetched: {species_taxonomy.get('species_id')}")
    return species_taxonomy



