# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Note: googledrive R package is a wrapper for Google Drive API.
# Python equivalent requires google-api-python-client.
# This code assumes credentials.json is present for OAuth2 flow.

# r2py:entity:drive_has_token
SCOPES = ['https://www.googleapis.com/auth/drive']
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)
service = build('drive', 'v3', credentials=creds)

# drive_create("WordStar", type = "document", starred = TRUE)
# r2py:entity:wordstar
file_metadata = {
    'name': 'WordStar',
    'mimeType': 'application/vnd.google-apps.document',
    'starred': True
}
wordstar = service.files().create(body=file_metadata, fields='files(starred)').execute()

# purrr::pluck(wordstar, "drive_resource", 1, "starred")
# r2py:entity:pluck
print(wordstar.get('files', [{}])[0].get('starred'))

# drive_create("ExecuVision", type = "presentation", description = "deeply nested bullet lists FTW")
# r2py:entity:execuvision
file_metadata = {
    'name': 'ExecuVision',
    'mimeType': 'application/vnd.google-apps.presentation',
    'description': 'deeply nested bullet lists FTW'
}
execuvision = service.files().create(body=file_metadata, fields='files(description)').execute()

# purrr::pluck(execuvision, "drive_resource", 1, "description")
# r2py:entity:pluck_1
print(execuvision.get('files', [{}])[0].get('description'))

# drive_browse(execuvision)
# Python approximation: print the webViewLink
# r2py:entity:drive_browse
file_info = service.files().get(fileId=execuvision.get('files', [{}])[0].get('id'), fields='webViewLink').execute()
print(file_info.get('webViewLink'))

# b4xl <- drive_mkdir("b4xl")
# r2py:entity:b4xl
folder_metadata = {
    'name': 'b4xl',
    'mimeType': 'application/vnd.google-apps.folder'
}
b4xl = service.files().create(body=folder_metadata, fields='id').execute()
b4xl_id = b4xl.get('id')

# drive_create("VisiCalc", path = b4xl, type = "spreadsheet")
# r2py:entity:drive_create
file_metadata = {
    'name': 'VisiCalc',
    'mimeType': 'application/vnd.google-apps.spreadsheet',
    'parents': [b4xl_id]
}
service.files().create(body=file_metadata).execute()

# drive_create("b4xl/SuperCalc", type = "spreadsheet")
# r2py:entity:drive_create_1
file_metadata = {
    'name': 'SuperCalc',
    'mimeType': 'application/vnd.google-apps.spreadsheet',
    'parents': [b4xl_id]
}
service.files().create(body=file_metadata).execute()

# drive_create("Lotus 1-2-3", path = "b4xl", type = "spreadsheet")
# R's path = "b4xl" searches for folder name. We use the cached b4xl_id.
# r2py:entity:drive_create_2
file_metadata = {
    'name': 'Lotus 1-2-3',
    'mimeType': 'application/vnd.google-apps.spreadsheet',
    'parents': [b4xl_id]
}
service.files().create(body=file_metadata).execute()

# drive_ls("b4xl")
# r2py:entity:drive_ls
query = f"'{b4xl_id}' in parents"
results = service.files().list(q=query, fields="files(id, name)").execute()
print(results.get('files', []))

# drive_create("VisiCalc", path = b4xl, overwrite = FALSE)
# Google Drive allows duplicate names. To prevent, we check existence first.
# r2py:entity:drive_create_3
check_query = f"name = 'VisiCalc' and '{b4xl_id}' in parents"
exists = service.files().list(q=check_query).execute().get('files', [])
if not exists:
    file_metadata = {'name': 'VisiCalc', 'mimeType': 'application/vnd.google-apps.spreadsheet', 'parents': [b4xl_id]}
    service.files().create(body=file_metadata).execute()

# drive_create("VisiCalc", path = b4xl, overwrite = TRUE)
# Overwrite in Drive usually means updating the content or deleting and recreating.
# r2py:entity:drive_create_4
check_query = f"name = 'VisiCalc' and '{b4xl_id}' in parents"
existing_files = service.files().list(q=check_query).execute().get('files', [])
for f in existing_files:
    service.files().delete(fileId=f['id']).execute()
file_metadata = {'name': 'VisiCalc', 'mimeType': 'application/vnd.google-apps.spreadsheet', 'parents': [b4xl_id]}
service.files().create(body=file_metadata).execute()

# drive_rm(wordstar, b4xl, execuvision)
# Extract IDs from the objects (handling the list structure of drive_create results)
# r2py:entity:drive_rm
ids_to_delete = [
    wordstar.get('files', [{}])[0].get('id'),
    b4xl_id,
    execuvision.get('files', [{}])[0].get('id')
]
for fid in ids_to_delete:
    if fid:
        service.files().delete(fileId=fid).execute()