# -*- coding: utf-8 -*-

import requests
import sys
import urllib.parse

sys.path.append('C:\\Users\\fatih\\source\\repos\\dinoai\\get_plant_info')
from get_species_info import get_species_info  # Tür bilgilerini almak için

API_KEY = '784ff879-2b92-4071-91ce-ca2de6f2415a'  # Tropicos API anahtarý
IMAGES_URL = 'https://services.tropicos.org/Name/{}/Images?apikey={}&format=json'

def get_name_id(scientific_name):
    scientific_name = scientific_name.strip()
    encoded_name = urllib.parse.quote(scientific_name)
    search_url = f'https://services.tropicos.org/Name/Search?name={encoded_name}&apikey={API_KEY}&format=json'

    response = requests.get(search_url)

    if response.status_code == 200:
        search_results = response.json()
        if search_results and len(search_results) > 0:
            name_id = search_results[0]['NameId']
            print(f"Found NameID for {scientific_name}: {name_id}")
            return name_id
    else:
        print(f"Error fetching NameID for {scientific_name}: {response.status_code}")
    return None

def get_images_by_name_id(name_id):
    images_url = IMAGES_URL.format(name_id, API_KEY)
    response = requests.get(images_url)

    if response.status_code == 200:
        images = response.json()
        print(f"Image response for NameID {name_id}: {images}")
        return images
    else:
        print(f"Error fetching images for NameID {name_id}: {response.status_code}")
        return []

def process_plant_images():
    species_list = get_species_info()

    for species in species_list:
        species_id, scientific_name = species

        name_id = get_name_id(scientific_name)
        if name_id:
            images = get_images_by_name_id(name_id)
            return species_id, images
        else:
            print(f"NameID not found for {scientific_name}")
            return None, None

if __name__ == "__main__":
    process_plant_images()
