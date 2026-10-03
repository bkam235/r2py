# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

import os
import pandas as pd
import numpy as np
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

# r2py:entity:drive_has_token
def drive_has_token():
    return os.path.exists('token.json')

# Setup for the session
if drive_has_token():
    creds = Credentials.from_authorized_user_file('token.json', scopes=['https://www.googleapis.com/auth/drive'])
    drive_service = build('drive', 'v3', credentials=creds)

# r2py:entity:wordstar
    # Helper to mimic drive_create with overwrite logic
    def drive_create_impl(name, path_val=None, type_val=None, description=None, starred=False, overwrite=None):
        mime_types = {
            "document": "application/vnd.google-apps.document",
            "presentation": "application/vnd.google-apps.presentation",
            "spreadsheet": "application/vnd.google-apps.spreadsheet",
            "folder": "application/vnd.google-apps.folder"
        }
        mime_type = mime_types.get(type_val, type_val)
        
        parents = []
        if path_val:
            # If path_val is a dict (dribble-like), get ID, else assume it's an ID or folder name
            p_id = path_val.get('id') if isinstance(path_val, dict) else path_val
            # Simplification: treat path as folder ID for parents
            parents = [p_id]

        # Overwrite logic
        query = f"name = '{name}' and trashed = false"
        if parents:
            query += f" and '{parents[0]}' in parents"
        
        existing = drive_service.files().list(q=query, fields="files(id)").execute().get('files', [])
        
        if existing:
            if overwrite is False:
                raise RuntimeError(f"File {name} already exists at target filepath")
            elif overwrite is True:
                for f in existing:
                    drive_service.files().update(fileId=f['id'], body={'trashed': True}).execute()
        
        metadata = {
            'name': name,
            'mimeType': mime_type,
            'starred': starred,
            'description': description,
            'parents': parents
        }
        # Clean None values
        metadata = {k: v for k, v in metadata.items() if v is not None}
        
        res = drive_service.files().create(body=metadata, fields='id, starred, description, drive_resource').execute()
        # Wrap in a structure similar to R's dribble/drive_resource
        return {'id': res.get('id'), 'name': name, 'drive_resource': [res]}

    # r2py:entity:wordstar
    wordstar = drive_create_impl("WordStar", type_val="document", starred=True)

    # r2py:entity:pluck
# r2py:entity:pluck
    print(wordstar['drive_resource'][0].get('starred'))

    # r2py:entity:execuvision
# r2py:entity:execuvision
    execuvision = drive_create_impl(
        "ExecuVision", 
        type_val="presentation", 
        description="deeply nested bullet lists FTW"
    )

    # r2py:entity:pluck_1
# r2py:entity:pluck_1
    print(execuvision['drive_resource'][0].get('description'))

    # r2py:entity:drive_browse
# r2py:entity:drive_browse
    print(f"https://drive.google.com/file/d/{execuvision['id']}/view")

    # r2py:entity:b4xl
# r2py:entity:b4xl
    b4xl = drive_create_impl("b4xl", type_val="folder")

    # r2py:entity:drive_create
# r2py:entity:drive_create
    drive_create_impl("VisiCalc", path_val=b4xl, type_val="spreadsheet")

    # r2py:entity:drive_create_1
    # R: drive_create("b4xl/SuperCalc", type = "spreadsheet")
# r2py:entity:drive_create_1
    drive_create_impl("SuperCalc", path_val=b4xl['id'], type_val="spreadsheet")

    # r2py:entity:drive_create_2
    # R: drive_create("Lotus 1-2-3", path = "b4xl", type = "spreadsheet")
    # We simulate finding the folder 'b4xl' by name first
# r2py:entity:drive_create_2
    b4xl_search = drive_service.files().list(q="name = 'b4xl' and mimeType = 'application/vnd.google-apps.folder'").execute()
    b4xl_id_from_name = b4xl_search.get('files', [{}])[0].get('id')
    drive_create_impl("Lotus 1-2-3", path_val=b4xl_id_from_name, type_val="spreadsheet")

    # r2py:entity:drive_ls
# r2py:entity:drive_ls
    query_ls = f"'{b4xl['id']}' in parents"
    ls_results = drive_service.files().list(q=query_ls, fields="files(id, name)").execute()
    print(ls_results.get('files', []))

    # r2py:entity:drive_create_3
# r2py:entity:drive_create_3
    try:
        drive_create_impl("VisiCalc", path_val=b4xl, overwrite=False)
    except RuntimeError as e:
        print(f"Caught expected error: {e}")

    # r2py:entity:drive_create_4
# r2py:entity:drive_create_4
    drive_create_impl("VisiCalc", path_val=b4xl, overwrite=True)

    # r2py:entity:drive_rm
# r2py:entity:drive_rm
    for item in [wordstar, b4xl, execuvision]:
        drive_service.files().delete(fileId=item['id']).execute()