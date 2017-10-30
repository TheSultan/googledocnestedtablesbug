import os
from os import path
import httplib2
from apiclient.http import MediaFileUpload
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import argparse

SCOPES = 'https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/documents'
CLIENT_SECRET_FILE = 'secret.json'
APPLICATION_NAME = 'upload_test'

def insert_media(service, dest_filename, description, parent_id, mime_type, media_content, dest_mime_type=None):
    media_body = MediaFileUpload(media_content, mimetype=mime_type, resumable=True)
    if dest_mime_type is None:
        dest_mime_type = mime_type
    body = {
        'name': dest_filename,
        'description': description,
        'mimeType': dest_mime_type,
    }
    # Set the parent folder.
    if parent_id:
        body['parents'] = [parent_id]

    file = service.files().create(
        body=body,
        media_body=media_body).execute()

    return file

parser = argparse.ArgumentParser(parents=[tools.argparser])
flags = parser.parse_args()
credential_path = 'test_auth.json'
store = oauth2client.file.Storage(credential_path)

print("Attempting to load credentials from %s" % credential_path)
credentials = store.get()
if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
    flow.user_agent = APPLICATION_NAME
    flow.params['access_type'] = 'offline'
    credentials = tools.run_flow(flow, store, flags)
    print('Storing credentials to ' + credential_path)

http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

doc_name = 'nested_tables'
uploaded_id = insert_media(drive_service, doc_name, doc_name, None, 
    'text/html', "nested_tables.html", dest_mime_type='application/vnd.google-apps.document')        
print("uploaded summary %s" % uploaded_id)

