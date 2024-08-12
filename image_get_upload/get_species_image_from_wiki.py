import requests
from get_species_info import get_species_info

def search_wikimedia_images(species_name):
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "generator": "search",
        "gsrsearch": species_name,
        "gsrlimit": "10",
        "iiprop": "url",
        "iiurlwidth": "500",  # Görsel boyutunu ayarlamak için
    }
    
    print(f"Requesting images for species: {species_name}")
    print(f"Request URL: {url}")
    print(f"Request Params: {params}")

    response = requests.get(url, params=params)
    
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response JSON: {data}")  # Tüm JSON yanýtý yazdýr

        pages = data.get("query", {}).get("pages", {})
        print(f"Pages Data: {pages}")  # Pages kýsmýný yazdýr
        
        image_urls = []
        
        for page_id, page_info in pages.items():
            print(f"Processing page ID: {page_id}")
            image_info = page_info.get("imageinfo", [])
            if image_info:
                image_url = image_info[0].get("thumburl")
                print(f"Found image URL: {image_url}")
                image_urls.append(image_url)
            else:
                print(f"No image info found for page ID: {page_id}")
        
        print(f"Total Images Found: {len(image_urls)}")
        return image_urls
    else:
        print(f"API request failed for {species_name} with status code: {response.status_code}")
        return []

if __name__ == "__main__":
    species_id = 1  # Buraya istediðiniz ID'yi girin; None tüm listeyi getirir
    species_info = get_species_info(species_id)
    
    if species_info:
        for species in species_info:
            species_name = species[1]
            print(f"Searching for images of species: {species_name}")
            image_urls = search_wikimedia_images(species_name)
            
            if image_urls:
                for i, url in enumerate(image_urls):
                    print(f"Image {i+1}: {url}")
            else:
                print("No images found.")
    else:
        print(f"No record found for Species ID {species_id}.")
