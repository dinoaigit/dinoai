import requests
import sys
import os

sys.path.append('C:\\Users\\fatih\\source\\repos\\dinoai\\get_plant_info')
from get_species_info import get_species_info

def get_inaturalist_images(taxon_name, per_page=10):
    print(f"Fetching iNaturalist data for: {taxon_name}")
    url = f"https://api.inaturalist.org/v1/observations"
    params = {
        'q': taxon_name,
        'per_page': per_page,
        'verifiable': True,
        'quality_grade': 'research'
    }

    # Send request to iNaturalist API
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"Data fetched successfully for: {taxon_name}")
        
        # Collect image URLs from observations
        images = []
        for observation in data['results']:
            if 'photos' in observation:
                for photo in observation['photos']:
                    images.append(photo['url'])
                    print(f"Image URL found: {photo['url']}")
        return images
    else:
        print(f"Error fetching data for {taxon_name}: {response.status_code}")
        return None

if __name__ == "__main__":
    # Fetch species info from the database
    print("Fetching species info from the database...")
    species_info = get_species_info()  # You can pass a specific species_id if needed
    
    if species_info:
        for species in species_info:
            species_name = species[1]  # Assuming name is at index 1
            print(f"\nProcessing species: {species_name}")

            # Fetch images for the species from iNaturalist
            image_urls = get_inaturalist_images(species_name, per_page=5)

            # If URLs are found, print them
            if image_urls:
                print(f"Image URLs for {species_name}:")
                for url in image_urls:
                    print(url)
            else:
                print(f"No images found for {species_name}")
    else:
        print("No species information found in the database.")
