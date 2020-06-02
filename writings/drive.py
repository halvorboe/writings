import io
import pickle
from pprint import pprint
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


import httplib2
import os, io

from apiclient import discovery
from apiclient.http import MediaFileUpload, MediaIoBaseDownload


SCOPES = ["https://www.googleapis.com/auth/drive"]


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("drive", "v3", credentials=creds)

    # Call the Drive v3 API
    results = (
        service.files()
        .list(pageSize=1000, fields="nextPageToken, files(id, name, parents)")
        .execute()
    )
    items = results.get("files", [])

    if not items:
        print("No files found.")
    else:
        print("Files:")
    for item in items:
        if "19s0Y5PhwKDewKGf46vNttXDotjpDisqQ" in item["parents"]:
            pprint(item)
            request = service.files().export_media(fileId=item["id"], mimeType='application/pdf')
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))


if __name__ == "__main__":
    main()

