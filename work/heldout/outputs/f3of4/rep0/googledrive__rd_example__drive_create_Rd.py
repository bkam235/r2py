# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, render, ui
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os

# Since 'googledrive' is a specialized R wrapper for the Google Drive API, 
# the Python equivalent is 'google-api-python-client'.
# This code assumes valid credentials are set up in a token.json file.

# Authentication setup
# r2py:entity:drive_has_token
def drive_has_token():
    return os.path.exists('token.json')

creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', scopes=['https://www.googleapis.com/auth/drive'])

if creds and creds.valid:
    service = build('drive', 'v3', credentials=creds)
else:
    # In a real scenario, trigger OAuth flow here
    service = None

if service:
    # wordstar <- drive_create("WordStar", type = "document", starred = TRUE)
# r2py:entity:wordstar
    wordstar_meta = {'name': 'WordStar', 'mimeType': 'application/vnd.google-apps.document', 'starred': True}
    wordstar = service.files().create(body=wordstar_meta, fields='id, starred').execute()

    # purrr::pluck(wordstar, "drive_resource", 1, "starred")
# r2py:entity:pluck
    print(wordstar.get('starred'))

    # execuvision <- drive_create("ExecuVision", type = "presentation", description = "deeply nested bullet lists FTW")
# r2py:entity:execuvision
    execuvision_meta = {
        'name': 'ExecuVision', 
        'mimeType': 'application/vnd.google-apps.presentation', 
        'description': 'deeply nested bullet lists FTW'
    }
    execuvision = service.files().create(body=execuvision_meta, fields='id, description').execute()

    # purrr::pluck(execuvision, "drive_resource", 1, "description")
# r2py:entity:pluck_1
    print(execuvision.get('description'))

    # drive_browse(execuvision)
    # Python equivalent: print the webViewLink
# r2py:entity:drive_browse
    execuvision_link = service.files().get(fileId=execuvision['id'], fields='webViewLink').execute()
    print(execuvision_link.get('webViewLink'))

    # b4xl <- drive_mkdir("b4xl")
# r2py:entity:b4xl
    b4xl_meta = {'name': 'b4xl', 'mimeType': 'application/vnd.google-apps.folder'}
    b4xl = service.files().create(body=b4xl_meta, fields='id').execute()
    b4xl_id = b4xl['id']

    # drive_create("VisiCalc", path = b4xl, type = "spreadsheet")
# r2py:entity:drive_create
    visicalc_meta = {'name': 'VisiCalc', 'mimeType': 'application/vnd.google-apps.spreadsheet', 'parents': [b4xl_id]}
    service.files().create(body=visicalc_meta).execute()

    # drive_create("b4xl/SuperCalc", type = "spreadsheet")
    # R's drive_create handles path strings; in Python we must specify parents explicitly
# r2py:entity:drive_create_1
    supercalc_meta = {'name': 'SuperCalc', 'mimeType': 'application/vnd.google-apps.spreadsheet', 'parents': [b4xl_id]}
    service.files().create(body=supercalc_meta).execute()

    # drive_create("Lotus 1-2-3", path = "b4xl", type = "spreadsheet")
    # Finding the folder ID for "b4xl" string
# r2py:entity:drive_create_2
    query = "name = 'b4xl' and mimeType = 'application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id)").execute()
    folder_id = results.get('files', [{}])[0].get('id')
    
    lotus_meta = {'name': 'Lotus 1-2-3', 'mimeType': 'application/vnd.google-apps.spreadsheet', 'parents': [folder_id]}
    service.files().create(body=lotus_meta).execute()

    # drive_ls("b4xl")
# r2py:entity:drive_ls
    ls_query = f"'{folder_id}' in parents"
    drive_ls = service.files().list(q=ls_query, fields="files(name)").execute()
    print(drive_ls.get('files'))

    # drive_create("VisiCalc", path = b4xl, overwrite = FALSE)
    # THIS WILL ERROR!
# r2py:entity:drive_create_3
    check_query = f"name = 'VisiCalc' and '{b4xl_id}' in parents"
    existing = service.files().list(q=check_query).execute()
    if existing.get('files'):
        raise FileExistsError("File already exists at target filepath (overwrite=FALSE)")
    else:
        visicalc_no_ov = {'name': 'VisiCalc', 'mimeType': 'application/vnd.google-apps.spreadsheet', 'parents': [b4xl_id]}
        service.files().create(body=visicalc_no_ov).execute()

    # drive_create("VisiCalc", path = b4xl, overwrite = TRUE)
    # Moves existing file to trash, then proceeds
# r2py:entity:drive_create_4
    existing = service.files().list(q=check_query).execute()
    if existing.get('files'):
        file_id = existing['files'][0]['id']
        service.files().update(fileId=file_id, body={'trashed': True}).execute()
    
    visicalc_ov = {'name': 'VisiCalc', 'mimeType': 'application/vnd.google-apps.spreadsheet', 'parents': [b4xl_id]}
    service.files().create(body=visicalc_ov).execute()

    # drive_rm(wordstar, b4xl, execuvision)
# r2py:entity:drive_rm
    service.files().delete(fileId=wordstar['id']).execute()
    service.files().delete(fileId=b4xl_id).execute()
    service.files().delete(fileId=execuvision['id']).execute()