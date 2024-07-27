from __future__ import print_function
import os.path
import pickle
import mimetypes

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = Credentials.from_authorized_user_info(pickle.load(token), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_777154597168-1jc5f2me1cal58c82eaiidbfgfshkamo.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds.to_json(), token)

    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file_to_drive(service, file_path, folder_id):
    file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
    mime_type, _ = mimetypes.guess_type(file_path)
    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("File ID: {}".format(file.get('id')))

def upload_folder_to_drive(service, folder_path, parent_folder_id=None):
    folder_metadata = {'name': os.path.basename(folder_path), 'mimeType': 'application/vnd.google-apps.folder'}
    if parent_folder_id:
        folder_metadata['parents'] = [parent_folder_id]
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    folder_id = folder.get('id')
    print("Folder ID: {}".format(folder_id))

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            upload_folder_to_drive(service, item_path, folder_id)
        else:
            upload_file_to_drive(service, item_path, folder_id)
