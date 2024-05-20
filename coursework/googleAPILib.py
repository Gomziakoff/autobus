import google.auth.exceptions
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import io
import os
from typing import List

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'key.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


def upload_file(folder_id:str,name:str,file_path:str) -> None:
    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': name,
        'parents': [folder_id]
    }
    try:
        media = MediaFileUpload(file_path, resumable=True)
        r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(r)
    except HttpError as err:
        if err.resp.status in [400]:
            print("Bad request error: Check your query parameters or syntax.")
            return
        else:
            print(f"An error occurred: {err}")
            print(f"maybe id:{folder_id} doesn't exist")
            return
    except FileNotFoundError as err:
        print(err)
        return
    except google.auth.exceptions.TransportError:
        print("Server not response")
        return


def get_folder_name(folder_id:str) -> str or None:
    # ------------- Build Service -------------
    service = build('drive', 'v3', credentials=credentials)
    try:
        return service.files().get(fileId=folder_id).execute()['name']
    except HttpError as err:
        if err.resp.status in [400]:
            print("Bad request error: Check your query parameters or syntax.")
            return
        else:
            print(f"An error occurred: {err}")
            print(f"maybe id:{folder_id} doesn't exist")
            return
    except google.auth.exceptions.TransportError:
        print("Server not response")
        return


def get_files_from_google_folder(folder_id:str) -> List[dict] or None:
    service = build('drive', 'v3', credentials=credentials)
    if folder_id:
        query = f"'{folder_id}' in parents"
        folder_name = get_folder_name(folder_id)
        if not folder_name:
            return
    else:
        query = ""
        folder_name = None
    try:
        results = service.files().list(
            q=query,
            pageSize=1000,
            fields="nextPageToken, files(id, name, mimeType, parents, fileExtension)").execute()
        items = results.get('files', [])
        return items
    except HttpError as err:
        if err.resp.status in [400]:
            print("Bad request error: Check your query parameters or syntax.")
            return
        else:
            print(f"An error occurred: {err}")
            print(f"maybe id:{folder_id} doesn't exist")
            return
    except google.auth.exceptions.TransportError:
        print("Server not response")
        return


def get_files_from_google_folders() -> List[dict] or None:
    service = build('drive', 'v3', credentials=credentials)
    try:
        results = service.files().list(
            pageSize=1000,
            fields="nextPageToken, files(id, name, mimeType, parents, fileExtension)").execute()
        nextPageToken = results.get('nextPageToken')
    except HttpError as err:
        if err.resp.status in [400]:
            print("Bad request error: Check your query parameters or syntax.")
            return
        else:
            print(f"An error occurred: {err}")
            return
    except google.auth.exceptions.TransportError:
        print("Server not response")
        return
    while nextPageToken:
        nextPage = service.files().list(pageSize=1000,
                                        fields="nextPageToken, files(id ,name, mimeType, parents, fileExtension)",
                                        pageToken=nextPageToken).execute()
        nextPageToken = nextPage.get('nextPageToken')
        results['files'] = results['files'] + nextPage['files']
    items = results.get('files', [])



def get_files_by_mimetype_google_folder(mimeType:str,folder_id:str) -> None:
    service = build('drive', 'v3', credentials=credentials)
    try:
        results = service.files().list(
            q=f"mimeType='{mimeType}' and '{folder_id}' in parents",
            pageSize=10,
            fields="nextPageToken, files(id, name, mimeType, parents, fileExtension)").execute()
        nextPageToken = results.get('nextPageToken')
    except HttpError as err:
        if err.resp.status in [400]:
            print("Bad request error: Check your query parameters or syntax.")
            return
        else:
            print(f"An error occurred: {err}")
            print(f"maybe id:{folder_id} doesn't exist")
            return
    except google.auth.exceptions.TransportError:
        print("Server not response")
        return
    while nextPageToken:
        nextPage = service.files().list(q=f"mimeType='{mimeType}' and '{folder_id}' in parents",
                                        pageSize=1000,
                                        fields="nextPageToken, files(id ,name, mimeType, parents, fileExtension)",
                                        pageToken=nextPageToken).execute()
        nextPageToken = nextPage.get('nextPageToken')
        results['files'] = results['files'] + nextPage['files']
    items = results.get('files', [])

    return items


def download_file(file_id:str, fold_name):
    service = build('drive', 'v3', credentials=credentials)
    filename = 'download/'+fold_name
    if not os.path.exists(filename):
        os.makedirs(filename)
    else:
        pass
    try:
        filename += service.files().get(fileId=file_id).execute()['name']
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Downloading {service.files().get(fileId=file_id).execute()['name']} %d%%." % int(status.progress() * 100))
    except HttpError as err:
        if err.resp.status in [400]:
            print("Bad request error: Check your query parameters or syntax.")
            return
        else:
            print(f"An error occurred: {err}")
            return
    except google.auth.exceptions.TransportError:
        print("Server not response")
        return

if __name__ == '__main__':
    download_file('1pApyURHRazNUeJRKdc')
    print(get_files_from_google_folder("1q9tAPkIM7NlLMiZhhYGafFdlMwsG7DWL"))