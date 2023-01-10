from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import json
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build


SERVICE_ACCOUNT_FILE = "google-credentials.json"

SCOPES = ["https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/drive.file" ]
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject="equipo@luteach.com"
)

service = build( "drive", "v3", credentials=credentials)


def create_folder(NAME, FOLDER_ID):
    """ Create a folder and prints the folder ID  """

    try:
        # create drive api client
        file_metadata = {
            'name': NAME,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [FOLDER_ID]
        }

        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, fields='id'
                                      ).execute()
        print(F'Folder ID: "{file.get("id")}".')
        return file.get('id')

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None

def upload_file(FILE_NAME, MIME_TYPE, FOLDER_ID):

    try:
        # Define the metadata for the file you want to upload
        metadata = {'name': FILE_NAME, 'parents': [FOLDER_ID]}

        # Create the MediaFileUpload object
        media = MediaFileUpload(FILE_NAME, mimetype=MIME_TYPE, chunksize=4*1024*1024, resumable=True)

        # Use the Drive API's files().create() method to upload the file
        request = service.files().create(body=metadata, media_body=media, fields='id')
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f'Uploaded {int(status.progress() * 100)}%')

        print(f'File with ID {response.get("id")} has been added to the folder with ID {FOLDER_ID}')

        return True
    except Exception as e:
        print(f"Error creating event: {e}")
        return False
