import pandas as pd
import numpy as np
from typing import Any, List, Dict, Optional

# Mocking the Google Drive API since actual authentication is not possible in this environment
class MockDriveResource:
    def __init__(self):
        self.files = []
        self.counter = 0

    def _generate_id(self):
        self.counter += 1
        return f"id_{self.counter}"

    class FileService:
        def __init__(self, outer):
            self.outer = outer

        def create(self, body=None, fields=None):
            def execute():
                name = body.get('name')
                parents = body.get('parents', [])
                
                # Check for overwrite logic simulation
                # In a real API, create doesn't check for existing names (Drive allows duplicates)
                # But googledrive R package adds this check.
                # We handle the overwrite logic in the wrapper functions.
                
                file_id = self.outer._generate_id()
                resource = {
                    'id': file_id,
                    'name': name,
                    'mimeType': body.get('mimeType'),
                    'starred': body.get('starred', False),
                    'description': body.get('description', ''),
                    'parents': parents,
                }
                self.outer.files.append(resource)
                
                if fields == '*':
                    return resource
                
                # Simple field filtering
                if fields:
                    return {k: v for k, v in resource.items() if k in fields.split(',')}
                return resource
            return type('Request', (), {'execute': execute})()

        def list(self, q=None, fields=None):
            def execute():
                results = []
                for f in self.outer.files:
                    # Simple query parsing for 'name =' and 'parents'
                    if q:
                        if f"name = '{f['name']}'" in q: pass 
                        # This is a simplification for the specific tests
                        if q and "in parents" in q:
                            # Extract ID from query like "'id_1' in parents"
                            parent_id = q.split("'")[1]
                            if parent_id not in f.get('parents', []):
                                continue
                    results.append(f)
                
                return {'files': results}
            return type('Request', (), {'execute': execute})()

        def get(self, fileId=None, fields=None):
            def execute():
                file = next((f for f in self.outer.files if f['id'] == fileId), None)
                if not file:
                    raise Exception("File not found")
                file['webViewLink'] = f"https://drive.google.com/file/d/{fileId}/view"
                if fields:
                    return {k: v for k, v in file.items() if k in fields.split(',')}
                return file
            return type('Request', (), {'execute': execute})()

        def delete(self, fileId=None):
            def execute():
                self.outer.files = [f for f in self.outer.files if f['id'] != fileId]
                return {}
            return type('Request', (), {'execute': execute})()

    def files(self):
        return self.FileService(self)

# Initialize Mock Drive
drive_api = MockDriveResource()
drive = drive_api

# r2py:entity:drive_has_token
def drive_has_token():
    # Simulating that we have a token
    return True

# r2py:entity:wordstar
def drive_mime_type(type_val):
    mapping = {
        "document": "application/vnd.google-apps.document",
        "presentation": "application/vnd.google-apps.presentation",
        "spreadsheet": "application/vnd.google-apps.spreadsheet",
        "folder": "application/vnd.google-apps.folder",
        "application/vnd.google-apps.folder": "application/vnd.google-apps.folder"
    }
    return mapping.get(type_val, type_val)

def drive_create(name=None, path=None, type=None, overwrite=None, **kwargs):
    # Logic to handle path/name rationalization from R source
    actual_name = name
    parent_id = None
    
    if path is not None:
        if isinstance(path, dict) and 'id' in path:
            parent_id = path['id']
        elif isinstance(path, str):
            if '/' in path:
                # Handle "b4xl/SuperCalc"
                parts = path.split('/')
                actual_name = parts[-1]
                # Find folder ID for the parent part
                folder = next((f for f in drive_api.files if f['name'] == parts[0]), None)
                if folder: parent_id = folder['id']
            else:
                # Handle path="b4xl"
                folder = next((f for f in drive_api.files if f['name'] == path), None)
                if folder: parent_id = folder['id']
                if name is None:
                    # If name is missing and path is provided, it's ambiguous in R,
                    # but here we assume the name is provided as the first arg.
                    pass

    # Overwrite logic
    if parent_id:
        existing = [f for f in drive_api.files if f['name'] == actual_name and parent_id in f.get('parents', [])]
    else:
        existing = [f for f in drive_api.files if f['name'] == actual_name]

    if existing:
        if overwrite is False:
            raise RuntimeError(f"File {actual_name} already exists")
        elif overwrite is True:
            for f in existing:
                drive.files().delete(fileId=f['id']).execute()

    mime = drive_mime_type(type)
    body = {
        'name': actual_name,
        'mimeType': mime,
        'parents': [parent_id] if parent_id else [],
        **kwargs
    }
    # R's starred = TRUE is passed in kwargs
    if 'starred' in kwargs:
        body['starred'] = kwargs['starred']
    if 'description' in kwargs:
        body['description'] = kwargs['description']

    res = drive.files().create(body=body, fields='*').execute()
    # R returns a 'dribble' (essentially a dataframe/list)
    return {'id': res['id'], 'name': res['name'], 'drive_resource': [res]}

# r2py:entity:b4xl
def drive_mkdir(name, path=None, overwrite=None, **kwargs):
    return drive_create(name=name, path=path, type="folder", overwrite=overwrite, **kwargs)

# r2py:entity:drive_ls
def drive_ls(path=None, **kwargs):
    if path is None:
        return drive.files().list().execute()
    
    parent_id = None
    if isinstance(path, str):
        folder = next((f for f in drive_api.files if f['name'] == path), None)
        if folder: parent_id = folder['id']
    elif isinstance(path, dict) and 'id' in path:
        parent_id = path['id']
    
    if parent_id:
        q = f"'{parent_id}' in parents"
        return drive.files().list(q=q).execute()
    return drive.files().list().execute()

# r2py:entity:drive_browse
def drive_browse(file):
    # file is a 'dribble'
    res = file['drive_resource'][0]
    link = drive.files().get(fileId=res['id'], fields='webViewLink').execute().get('webViewLink')
    print(link)
    return link

# r2py:entity:drive_rm
def drive_rm(*args, **kwargs):
    for item in args:
        if isinstance(item, dict) and 'id' in item:
            drive.files().delete(fileId=item['id']).execute()

# r2py:entity:pluck
def pluck(x, *args):
    # Simple nested get
    val = x
    for key in args:
        if isinstance(val, list):
            val = val[key]
        elif isinstance(val, dict):
            val = val.get(key)
        else:
            return None
    return val

# MAIN EXECUTION
if drive_has_token():
    # wordstar <- drive_create("WordStar", type = "document", starred = TRUE)
# r2py:entity:wordstar
    wordstar = drive_create("WordStar", type="document", starred=True)

    # purrr::pluck(wordstar, "drive_resource", 1, "starred")
# r2py:entity:pluck
    starred_status = pluck(wordstar, "drive_resource", 0, "starred")

    # execuvision <- drive_create("ExecuVision", type = "presentation", description = "deeply nested bullet lists FTW")
# r2py:entity:execuvision
    execuvision = drive_create(
        "ExecuVision", 
        type="presentation", 
        description="deeply nested bullet lists FTW"
    )

    # purrr::pluck(execuvision, "drive_resource", 1, "description")
# r2py:entity:pluck_1
    description_val = pluck(execuvision, "drive_resource", 0, "description")

    # drive_browse(execuvision)
# r2py:entity:drive_browse
    drive_browse(execuvision)

    # b4xl <- drive_mkdir("b4xl")
# r2py:entity:b4xl
    b4xl = drive_mkdir("b4xl")

    # drive_create("VisiCalc", path = b4xl, type = "spreadsheet")
# r2py:entity:drive_create
    drive_create("VisiCalc", path=b4xl, type="spreadsheet")

    # drive_create("b4xl/SuperCalc", type = "spreadsheet")
# r2py:entity:drive_create_1
    drive_create("b4xl/SuperCalc", type="spreadsheet")

    # drive_create("Lotus 1-2-3", path = "b4xl", type = "spreadsheet")
# r2py:entity:drive_create_2
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # drive_ls("b4xl")
# r2py:entity:drive_ls
    drive_ls("b4xl")

    # drive_create("VisiCalc", path = b4xl, overwrite = FALSE)
    # THIS SHOULD ERROR
    try:
# r2py:entity:drive_create_3
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except RuntimeError as e:
        print(f"Caught expected error: {e}")

    # drive_create("VisiCalc", path = b4xl, overwrite = TRUE)
# r2py:entity:drive_create_4
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # drive_rm(wordstar, b4xl, execuvision)
# r2py:entity:drive_rm
    drive_rm(wordstar, b4xl, execuvision)