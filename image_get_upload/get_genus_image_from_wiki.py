import requests
from get_genus_info import get_genus_info  # `get_genus_info.py` dosyasýndan fonksiyonu alýyoruz

def search_wikimedia_images(genus_name):
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "generator": "search",
        "gsrsearch": genus_name,
        "gsrlimit": "10",
        "iiprop": "url",
        "iiurlwidth": "500",  # Görsel boyutunu ayarlamak için
    }
    
    print(f"Requesting images for genus: {genus_name}")
    print(f"Request URL: {url}")
    print(f"Request Params: {params}")

    response = requests.get(url, params=params)
    
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response JSON: {data}")  # Tüm JSON yanýtýný yazdýr

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
        print(f"API request failed for {genus_name} with status code: {response.status_code}")
        return []

if __name__ == "__main__":
    genus_id = 150  # Buraya istediðiniz ID'yi girin; None tüm listeyi getirir
    genus_info = get_genus_info(genus_id)
    
    if genus_info:
        for genus in genus_info:
            genus_name = genus[1]
            print(f"Searching for images of genus: {genus_name}")
            image_urls = search_wikimedia_images(genus_name)
            
            if image_urls:
                for i, url in enumerate(image_urls):
                    print(f"Image {i+1}: {url}")
            else:
                print("No images found.")
    else:
        print(f"No record found for Genus ID {genus_id}.")

