# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render
# Note: googledrive R package maps to Google Drive API (google-api-python-client)
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Initialization of Drive service
# Assuming GOOGLE_APPLICATION_CREDENTIALS environment variable is set
drive_service = build('drive', 'v3')

# r2py:entity:drive_has_token
# Equivalent of drive_has_token() / authentication check
try:
    # examplesIf logic
# r2py:entity:wordstar
    # drive_create("WordStar", type = "document", starred = TRUE)
    wordstar_metadata = {
        'name': 'WordStar',
        'mimeType': 'application/vnd.google-apps.document',
        'starred': True
    }
    wordstar = drive_service.files().create(body=wordstar_metadata, fields='files(id, starred)').execute()

# r2py:entity:pluck
    # purrr::pluck(wordstar, "drive_resource", 1, "starred")
    print(wordstar['files'][0].get('starred'))

# r2py:entity:execuvision
    # drive_create("ExecuVision", type = "presentation", description = "deeply nested bullet lists FTW")
    execuvision_metadata = {
        'name': 'ExecuVision',
        'mimeType': 'application/vnd.google-apps.presentation',
        'description': 'deeply nested bullet lists FTW'
    }
    execuvision = drive_service.files().create(body=execuvision_metadata, fields='files(id, description)').execute()

# r2py:entity:pluck_1
    # purrr::pluck(execuvision, "drive_resource", 1, "description")
    print(execuvision['files'][0].get('description'))

# r2py:entity:drive_browse
    # drive_browse(execuvision)
    # Python approximation: printing the webViewLink
    execuvision_link = drive_service.files().get(fileId=execuvision['files'][0]['id'], fields='webViewLink').execute()
    print(execuvision_link.get('webViewLink'))

# r2py:entity:b4xl
    # b4xl <- drive_mkdir("b4xl")
    b4xl_metadata = {
        'name': 'b4xl',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    b4xl = drive_service.files().create(body=b4xl_metadata, fields='files(id)').execute()
    b4xl_id = b4xl['files'][0]['id']

# r2py:entity:drive_create
    # drive_create("VisiCalc", path = b4xl, type = "spreadsheet")
    visicalc_metadata = {
        'name': 'VisiCalc',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [b4xl_id]
    }
    drive_service.files().create(body=visicalc_metadata).execute()

# r2py:entity:drive_create_1
    # drive_create("b4xl/SuperCalc", type = "spreadsheet")
    supercalc_metadata = {
        'name': 'SuperCalc',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [b4xl_id]
    }
    drive_service.files().create(body=supercalc_metadata).execute()

# r2py:entity:drive_create_2
    # drive_create("Lotus 1-2-3", path = "b4xl", type = "spreadsheet")
    lotus_metadata = {
        'name': 'Lotus 1-2-3',
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        'parents': [b4xl_id]
    }
    drive_service.files().create(body=lotus_metadata).execute()

# r2py:entity:drive_ls
    # drive_ls("b4xl")
    query = f"'{b4xl_id}' in parents"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    print(results.get('files', []))

# r2py:entity:drive_create_3
    # drive_create("VisiCalc", path = b4xl, overwrite = FALSE)
    # Check if exists first to simulate overwrite = FALSE
    check_query = f"name = 'VisiCalc' and '{b4xl_id}' in parents"
    exists = drive_service.files().list(q=check_query).execute().get('files', [])
    if not exists:
        drive_service.files().create(body=visicalc_metadata).execute()

# r2py:entity:drive_create_4
    # drive_create("VisiCalc", path = b4xl, overwrite = TRUE)
    # If exists, update name or replace; otherwise create
    if exists:
        drive_service.files().update(fileId=exists[0]['id'], body={'name': 'VisiCalc'}).execute()
    else:
        drive_service.files().create(body=visicalc_metadata).execute()

# r2py:entity:drive_rm
    # drive_rm(wordstar, b4xl, execuvision)
    drive_service.files().delete(fileId=wordstar['files'][0]['id']).execute()
    drive_service.files().delete(fileId=b4xl_id).execute()
    drive_service.files().delete(fileId=execuvision['files'][0]['id']).execute()

except Exception as e:
    print(f"Authentication failed or error occurred: {e}")