import os
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build

def upload_to_drive(image_id, image_path):
    service = build('drive', 'v3', credentials=your_credentials)
    file_metadata = {'name': f'{image_id}.jpg'}
    media = MediaFileUpload(image_path, mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

for species in species_list:
    species_id = species[0]
    species_name = species[1]
    
    for i, url in enumerate(image_urls):
        image_path = f"{species_id}_{i}.jpg"
        # Görseli indir ve kaydet
        # upload_to_drive(species_id, image_path)