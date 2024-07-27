from flask import Flask, redirect, url_for, session, request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

CLIENT_SECRETS_FILE = "client_secret_1056700496812-789gr4b175ip8361501pmd25bn9qumsk.apps.googleusercontent.com.json"
SCOPES = ['https://www.googleapis.com/auth/drive.file']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri='https://dinoai.org/oauth2callback'
)

@app.route('/')
def index():
    return 'Google OAuth 2.0 ile Otomatik Giriş! <a href="/login">Giriş Yap</a>'

@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    flow.fetch_token(authorization_response=request.url)
    if not session['state'] == request.args['state']:
        return redirect(url_for('index'))
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    return redirect(url_for('drive'))

@app.route('/drive')
def drive():
    if 'credentials' not in session:
        return redirect('login')

    credentials = google.oauth2.credentials.Credentials(
        **session['credentials']
    )

    drive_service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    folder_metadata = {
        'name': 'DinoAI_Folder',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()

    return f'Folder created with ID: {folder.get("id")}'

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

if __name__ == '__main__':
    app.run()
