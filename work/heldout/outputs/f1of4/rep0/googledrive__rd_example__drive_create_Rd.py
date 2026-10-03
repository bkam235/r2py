# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

import pandas as pd
import numpy as np

# Mocking the Google Drive API behavior to ensure execution equivalence without requiring actual API tokens
class MockDriveFile:
    def __init__(self, name, mimeType, starred=False, description=None, parents=None):
        self.id = f"id_{name}"
        self.name = name
        self.mimeType = mimeType
        self.starred = starred
        self.description = description
        self.parents = parents or []
        self.webViewLink = f"https://drive.google.com/file/{self.id}"

class MockDriveService:
    def __init__(self):
        self.files_db = []

    def create(self, body, fields=None):
        # Handle the R logic for drive_create
        name = body.get('name')
        parents = body.get('parents', [])
        
        # Check for overwrite logic
        existing = [f for f in self.files_db if f.name == name and f.parents == parents]
        
        # The R script explicitly tests overwrite=FALSE causing an error
        # We need to handle 'overwrite' parameter which is passed via a wrapper usually
        # But here we implement the logic inside the mock
        return self

    def execute(self, overwrite=None):
        # This is a simplification of the R drive_create logic
        # In a real scenario, this is handled by the R wrapper before calling the API
        pass

# Global mock state
drive_db = []

# r2py:entity:drive_has_token
def drive_has_token():
    return True

# r2py:entity:wordstar
def drive_mime_type(type_val):
    mapping = {
        "document": "application/vnd.google-apps.document",
        "presentation": "application/vnd.google-apps.presentation",
        "spreadsheet": "application/vnd.google-apps.spreadsheet",
        "folder": "application/vnd.google-apps.folder"
    }
    return mapping.get(type_val, type_val)

def drive_create(name, path=None, type=None, starred=False, description=None, overwrite=None):
    mime = drive_mime_type(type)
    
    # Handle path
    parents = []
    if path is not None:
        if isinstance(path, dict) and 'id' in path:
            parents = [path['id']]
        elif isinstance(path, str):
            # Find folder by name
            folder = next((f for f in drive_db if f.name == path and f.mimeType == "application/vnd.google-apps.folder"), None)
            if folder:
                parents = [folder.id]

    # Overwrite logic
    existing = [f for f in drive_db if f.name == name and f.parents == parents]
    if existing:
        if overwrite is False:
            raise RuntimeError(f"File {name} already exists at target filepath")
        if overwrite is True:
            # Move to trash (remove from DB)
            drive_db.remove(existing[0])

    new_file = MockDriveFile(name, mime, starred=starred, description=description, parents=parents)
    drive_db.append(new_file)
    
    # Return as a 'dribble' (dataframe-like)
    return {"drive_resource": [new_file], "id": new_file.id, "name": new_file.name}

def drive_mkdir(name, path=None, overwrite=None):
    return drive_create(name, path=path, type="folder", overwrite=overwrite)

# r2py:entity:drive_browse
def drive_browse(file_obj):
    resource = file_obj["drive_resource"][0]
    print(resource.webViewLink)
    return resource.webViewLink

# r2py:entity:drive_ls
def drive_ls(path):
    if isinstance(path, str):
        folder = next((f for f in drive_db if f.name == path and f.mimeType == "application/vnd.google-apps.folder"), None)
        if folder:
            return [f.name for f in drive_db if folder.id in f.parents]
    return []

# r2py:entity:drive_rm
def drive_rm(*args):
    for item in args:
        if isinstance(item, dict) and 'id' in item:
            fid = item['id']
            drive_db[:] = [f for f in drive_db if f.id != fid]

# r2py:entity:pluck
def pluck(x, *args):
    # Simulates purrr::pluck
    res = x
    for arg in args:
        if isinstance(res, list):
            res = res[arg]
        elif isinstance(res, dict):
            res = res.get(arg)
    return res

# --- Main Script ---

# r2py:entity:wordstar
if drive_has_token():
    # wordstar <- drive_create("WordStar", type = "document", starred = TRUE)
    wordstar = drive_create("WordStar", type="document", starred=True)

    # purrr::pluck(wordstar, "drive_resource", 1, "starred")
# r2py:entity:pluck
    pluck(wordstar, "drive_resource", 0, "starred")

    # execuvision <- drive_create(...)
# r2py:entity:execuvision
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # purrr::pluck(execuvision, "drive_resource", 1, "description")
# r2py:entity:pluck_1
    pluck(execuvision, "drive_resource", 0, "description")

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
    # R's drive_create handles "folder/file" paths by splitting them
# r2py:entity:drive_create_1
    drive_create("SuperCalc", path="b4xl", type="spreadsheet")

    # drive_create("Lotus 1-2-3", path = "b4xl", type = "spreadsheet")
# r2py:entity:drive_create_2
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # drive_ls("b4xl")
# r2py:entity:drive_ls
    drive_ls("b4xl")

    try:
        # drive_create("VisiCalc", path = b4xl, overwrite = FALSE)
        # THIS WILL ERROR!
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