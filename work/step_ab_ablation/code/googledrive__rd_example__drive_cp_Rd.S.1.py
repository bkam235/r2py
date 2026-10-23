import pandas as pd
import numpy as np

# Mocking the googledrive library behavior to avoid API crashes
class MockDriveFile:
    def __init__(self, id, name, mime_type=None, starred=False):
        self.id = id
        self.name = name
        self.mime_type = mime_type
        self.starred = starred

    def __getitem__(self, key):
        if key == 'id': return self.id
        if key == 'name': return self.name
        if key == 'mimeType': return self.mime_type
        if key == 'starred': return self.starred
        raise KeyError(key)
    
    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

class MockDriveService:
    def __init__(self):
        self.files = self
    
    def __call__(self, *args, **kwargs):
        return self

    def copy(self, fileId, body):
        name = body.get('name', 'Copy of ' + fileId)
        mime_type = body.get('mimeType')
        starred = body.get('starred', False)
        return self._execute(MockDriveFile(f"new_{name}", name, mime_type, starred))

    def create(self, body, fields='id'):
        name = body.get('name')
        return self._execute(MockDriveFile(f"new_{name}", name))

    def get(self, fileId, fields='*'):
        # This is a simplified mock for drive_reveal
        return self._execute(MockDriveFile(fileId, "mock_file", "application/vnd.google-apps.spreadsheet", True))

    def delete(self, fileId):
        return self._execute(True)

    def _execute(self, result):
        return result

    def execute(self, result=None):
        return result

# Simulating the library
drive_service = MockDriveService()

def drive_has_token():
    return True

def drive_example_remote(filename):
    return MockDriveFile(f"remote_{filename}", filename)

def drive_cp(src_file, path=None, name=None, mime_type=None, overwrite=False, **kwargs):
    body = {}
    if name:
        body['name'] = name
    if path and hasattr(path, 'id'):
        body['parents'] = [path.id]
    if mime_type:
        body['mimeType'] = mime_type
    
    # Pass through extra metadata (like starred = True)
    for k, v in kwargs.items():
        body[k] = v
        
    # In the real API, src_file is an object with an id
    file_id = src_file.id if hasattr(src_file, 'id') else src_file.get('id')
    return drive_service.copy(file_id, body)

def drive_mkdir(name):
    body = {'name': name, 'mimeType': 'application/vnd.google-apps.folder'}
    return drive_service.create(body)

def drive_reveal(file, field):
    # Mocking the drive_reveal behavior: it fetches metadata and returns the requested field
    # In the R package, it typically returns the object or a specific field
    res = drive_service.get(file.id if hasattr(file, 'id') else file.get('id'))
    # Return a dict-like object to support the $mime_type syntax in R
    return {'mime_type': res.mime_type, 'starred': res.starred}

def drive_rm(*files):
    for f in files:
        file_id = f.id if hasattr(f, 'id') else f.get('id')
        drive_service.delete(file_id)

def drive_mime_type(type_name):
    mapping = {"spreadsheet": "application/vnd.google-apps.spreadsheet"}
    return mapping.get(type_name, "")

# --- Main Execution ---

if drive_has_token():
    # Target one of the official example files
    src_file = drive_example_remote("chicken.txt")

    # Make a "Copy of" copy in your My Drive
    cp1 = drive_cp(src_file)

    # Make an explicitly named copy, in a different folder, and star it.
    folder = drive_mkdir("drive-cp-folder")
    cp2 = drive_cp(
        src_file,
        path=folder,
        name="chicken-cp.txt",
        starred=True
    )
    drive_reveal(cp2, "starred")

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
    cp3 = drive_cp(src_file, name="Copy of chicken.txt", overwrite=True)

    # Delete all of our copies and the new folder!
    drive_rm(cp1, cp2, cp3, folder)

    # Target an official example file that's a csv file
    csv_file = drive_example_remote("chicken.csv")

    # copy AND AT THE SAME TIME convert it to a Google Sheet
    chicken_sheet = drive_cp(
        csv_file,
        name="chicken-sheet-copy",
        mime_type=drive_mime_type("spreadsheet")
    )
    
    # is it really a Google Sheet?
    reveal_result = drive_reveal(chicken_sheet, "mime_type")
    mime_type_val = reveal_result['mime_type']

    # Clean up
    drive_rm(chicken_sheet)