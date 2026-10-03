import pandas as pd
import numpy as np

# Mocking the Google Drive API and googledrive R package behavior
# since we cannot perform real OAuth2 flows in this environment.

class DriveFile:
    def __init__(self, name, file_id, mime_type, starred=False, description=None, parents=None):
        self.id = file_id
        self.name = name
        self.mime_type = mime_type
        self.starred = starred
        self.description = description
        self.parents = parents or []
        self.drive_resource = {"id": self.id, "name": self.name, "mimeType": self.mime_type, 
                               "starred": self.starred, "description": self.description}

class MockDriveService:
    def __init__(self):
        self.files = []
        self.counter = 0

    def create(self, name, type=None, starred=False, description=None, path=None, overwrite=None):
        # Handle path logic
        parent_id = None
        if isinstance(path, DriveFile):
            parent_id = path.id
        elif isinstance(path, str):
            # Basic mock: find folder by name
            for f in self.files:
                if f.name == path and f.mime_type == 'application/vnd.google-apps.folder':
                    parent_id = f.id
                    break
        
        # Check for existing file at path
        existing = [f for f in self.files if f.name == name and (not parent_id or parent_id in f.parents)]
        
        if existing:
            if overwrite is False:
                raise FileExistsError(f"File {name} already exists")
            if overwrite is True:
                # Trash existing (mocked by removing from list)
                self.files = [f for f in self.files if f != existing[0]]
        
        # Mime type mapping
        mime_map = {
            "document": "application/vnd.google-apps.document",
            "presentation": "application/vnd.google-apps.presentation",
            "spreadsheet": "application/vnd.google-apps.spreadsheet",
            "folder": "application/vnd.google-apps.folder"
        }
        mime_type = mime_map.get(type, type)
        
        self.counter += 1
        new_file = DriveFile(name, f"id_{self.counter}", mime_type, starred, description, [parent_id] if parent_id else [])
        self.files.append(new_file)
        return new_file

    def list_files(self, path=None):
        if path is None:
            return self.files
        if isinstance(path, DriveFile):
            return [f for f in self.files if path.id in f.parents]
        if isinstance(path, str):
            folder = next((f for f in self.files if f.name == path), None)
            if folder:
                return [f for f in self.files if folder.id in f.parents]
        return []

    def delete(self, *files):
        for f in files:
            if f in self.files:
                self.files.remove(f)

drive_service = MockDriveService()

# r2py:entity:drive_has_token
def drive_has_token():
    return True

# r2py:entity:wordstar
def drive_create(name, path=None, type=None, starred=False, description=None, overwrite=None):
    return drive_service.create(name, type, starred, description, path, overwrite)

# r2py:entity:b4xl
def drive_mkdir(name, path=None, overwrite=None):
    return drive_create(name, path=path, type="folder", overwrite=overwrite)

# r2py:entity:drive_ls
def drive_ls(path=None):
    return drive_service.list_files(path)

# r2py:entity:drive_browse
def drive_browse(file):
    print(f"Browsing file: {file.name} (ID: {file.id})")
    return file.id

# r2py:entity:drive_rm
def drive_rm(*files):
    drive_service.delete(*files)

# r2py:entity:pluck
def pluck(obj, *keys):
    # Mock purrr::pluck logic
    val = obj
    if isinstance(val, DriveFile):
        val = val.drive_resource
    for key in keys:
        if isinstance(val, list):
            val = val[int(key)]
        elif isinstance(val, dict):
            val = val.get(key)
        else:
            return None
    return val

# --- Main Execution ---

# r2py:entity:drive_has_token
if drive_has_token():
    # Create a blank Google Doc named 'WordStar'
# r2py:entity:wordstar
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred?
# r2py:entity:pluck
    print(pluck(wordstar, "starred"))

    # Create a blank Google Slides presentation
# r2py:entity:execuvision
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description?
# r2py:entity:pluck_1
    print(pluck(execuvision, "description"))

    # check out the new presentation
# r2py:entity:drive_browse
    drive_browse(execuvision)

    # Create folder 'b4xl'
# r2py:entity:b4xl
    b4xl = drive_mkdir("b4xl")
# r2py:entity:drive_create
    drive_create("VisiCalc", path=b4xl, type="spreadsheet")

    # Another way to create a Google Sheet in 'b4xl'
    # R: drive_create("b4xl/SuperCalc", ...)
# r2py:entity:drive_create_1
    drive_create("SuperCalc", path="b4xl", type="spreadsheet")

    # Yet another way to create a new file in a folder
# r2py:entity:drive_create_2
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # Did we really create those Sheets in the intended folder?
# r2py:entity:drive_ls
    print(drive_ls("b4xl"))

    # `overwrite = FALSE` errors if file already exists
    try:
# r2py:entity:drive_create_3
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except FileExistsError as e:
        print(f"Caught expected error: {e}")

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
# r2py:entity:drive_create_4
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
# r2py:entity:drive_rm
    drive_rm(wordstar, b4xl, execuvision)