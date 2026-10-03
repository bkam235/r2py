import pandas as pd
import numpy as np
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

# Setup Google Drive API client
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        # In a real environment, credentials.json must exist
        try:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        except Exception:
            creds = None
    if creds:
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

drive_service = build('drive', 'v3', credentials=creds) if creds else None

# Wrapper for drive_has_token behavior
# r2py:entity:drive_has_token
def drive_has_token():
    return creds is not None

if drive_has_token():
    # drive_create("WordStar", type = "document", starred = TRUE)
# r2py:entity:wordstar
    file_metadata = {
        'name': 'WordStar',
        'mimeType': 'application/vnd.google-apps.document',
        'starred': True
    }
    wordstar = drive_service.files().create(body=file_metadata, fields='id, starred').execute()

    # purrr::pluck(wordstar, "drive_resource", 1, "starred")
# r2py:entity:pluck
    print(wordstar.get('starred'))

    # drive_create("ExecuVision", type = "presentation", description = "deeply nested bullet lists FTW")
# r2py:entity:execuvision
    file_metadata = {
        'name': 'ExecuVision',
        'mimeType': 'application/vnd.google-apps.presentation',
        'description': 'deeply nested bullet lists FTW'
    }
    execuvision = drive_service.files().create(body=file_metadata, fields='id, description').execute()

    # purrr::pluck(execuvision, "drive_resource", 1, "description")
# r2py:entity:pluck_1
    print(execuvision.get('description'))

    # drive_browse(execuvision)
# r2py:entity:drive_browse
    res = drive_service.files().get(fileId=execuvision['id'], fields='webViewLink').execute()
    print(res.get('webViewLink'))

    # drive_mkdir("b4xl")
# r2py:entity:b4xl
    file_metadata = {
        'name': 'b4xl',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    b4xl = drive_service.files().create(body=file_metadata, fields='id').execute()
    b4xl_id = b4xl['id']

    # drive_create("VisiCalc", path = b4xl, type = "spreadsheet")
# r2py:entity:drive_create
    file_metadata = {
        'name': 'VisiCalc',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [b4xl_id]
    }
    drive_service.files().create(body=file_metadata).execute()

    # drive_create("b4xl/SuperCalc", type = "spreadsheet")
# r2py:entity:drive_create_1
    file_metadata = {
        'name': 'SuperCalc',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [b4xl_id]
    }
    drive_service.files().create(body=file_metadata).execute()

    # drive_create("Lotus 1-2-3", path = "b4xl", type = "spreadsheet")
# r2py:entity:drive_create_2
    file_metadata = {
        'name': 'Lotus 1-2-3',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [b4xl_id]
    }
    drive_service.files().create(body=file_metadata).execute()

    # drive_ls("b4xl")
# r2py:entity:drive_ls
    query = f"'{b4xl_id}' in parents"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    print(results.get('files', []))

    # drive_create("VisiCalc", path = b4xl, overwrite = FALSE)
    # THIS WILL ERROR! (Force an exception if file exists)
# r2py:entity:drive_create_3
    query = f"name = 'VisiCalc' and '{b4xl_id}' in parents and trashed = false"
    exists = drive_service.files().list(q=query).execute().get('files', [])
    if exists:
        raise FileExistsError("File already exists at target filepath (overwrite = FALSE)")
    else:
        file_metadata = {'name': 'VisiCalc', 'mimeType': 'application/vnd.google-apps.spreadsheet', 'parents': [b4xl_id]}
        drive_service.files().create(body=file_metadata).execute()

    # drive_create("VisiCalc", path = b4xl, overwrite = TRUE)
# r2py:entity:drive_create_4
    query = f"name = 'VisiCalc' and '{b4xl_id}' in parents and trashed = false"
    exists = drive_service.files().list(q=query).execute().get('files', [])
    if exists:
        # Move existing file to trash then create new
        drive_service.files().update(fileId=exists[0]['id'], body={'trashed': True}).execute()
    
    file_metadata = {'name': 'VisiCalc', 'mimeType': 'application/vnd.google-apps.spreadsheet', 'parents': [b4xl_id]}
    drive_service.files().create(body=file_metadata).execute()

    # drive_rm(wordstar, b4xl, execuvision)
# r2py:entity:drive_rm
    for item in [wordstar, b4xl, execuvision]:
        fid = item['id']
        drive_service.files().update(fileId=fid, body={'trashed': True}).execute()