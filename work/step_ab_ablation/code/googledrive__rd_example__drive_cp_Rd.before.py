# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

import pandas as pd
import numpy as np
from plotnine import *
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import io

# Note: googledrive R package maps to Google Drive API v3.
# This implementation assumes valid credentials are present in token.json
creds = Credentials.from_authorized_user_file('token.json', scopes=['https://www.googleapis.com/auth/drive'])
drive_service = build('drive', 'v3', credentials=creds)

# r2py:entity:drive_has_token
def drive_has_token():
    return creds is not None

if drive_has_token():
    # examplesIf
# r2py:entity:src_file
    # drive_example_remote is a helper for internal R examples; we simulate with a known ID or placeholder
    src_file = {'id': 'chicken_txt_id_placeholder', 'name': 'chicken.txt'}

# r2py:entity:cp1
    # cp1 <- drive_cp(src_file)
    cp1_meta = {'name': src_file['name']}
    cp1 = drive_service.files().copy(fileId=src_file['id'], body=cp1_meta).execute()

# r2py:entity:folder
    # folder <- drive_mkdir("drive-cp-folder")
    folder_meta = {'name': 'drive-cp-folder', 'mimeType': 'application/vnd.google-apps.folder'}
    folder = drive_service.files().create(body=folder_meta, fields='id').execute()

# r2py:entity:cp2
    # cp2 <- drive_cp(...)
    cp2_meta = {
        'name': 'chicken-cp.txt',
        'parents': [folder['id']],
        'starred': True
    }
    cp2 = drive_service.files().copy(fileId=src_file['id'], body=cp2_meta).execute()
    
# r2py:entity:drive_reveal
    # drive_reveal(cp2, "starred")
    cp2_reveal = drive_service.files().get(fileId=cp2['id'], fields='starred').execute()
    print(cp2_reveal.get('starred'))

# r2py:entity:cp3
    # cp3 <- drive_cp(src_file, name = "Copy of chicken.txt", overwrite = TRUE)
    # Google Drive API doesn't have a direct 'overwrite' flag for copy; 
    # it usually involves searching for existing file and deleting/updating.
    cp3_meta = {'name': 'Copy of chicken.txt'}
    cp3 = drive_service.files().copy(fileId=src_file['id'], body=cp3_meta).execute()

# r2py:entity:drive_rm
    # drive_rm(cp1, cp2, cp3, folder)
    for item in [cp1['id'], cp2['id'], cp3['id'], folder['id']]:
        drive_service.files().delete(fileId=item).execute()

# r2py:entity:csv_file
    # (csv_file <- drive_example_remote("chicken.csv"))
    csv_file = {'id': 'chicken_csv_id_placeholder', 'name': 'chicken.csv'}

# r2py:entity:chicken_sheet
    # chicken_sheet <- drive_cp(...)
    chicken_sheet_meta = {
        'name': 'chicken-sheet-copy',
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }
    chicken_sheet = drive_service.files().copy(
        fileId=csv_file['id'], 
        body=chicken_sheet_meta
    ).execute()

# r2py:entity:drive_reveal_1
    # drive_reveal(chicken_sheet, "mime_type")$mime_type
    chicken_sheet_reveal = drive_service.files().get(fileId=chicken_sheet['id'], fields='mimeType').execute()
    print(chicken_sheet_reveal.get('mimeType'))

# r2py:entity:drive_rm_1
    # drive_rm(chicken_sheet)
    drive_service.files().delete(fileId=chicken_sheet['id']).execute()