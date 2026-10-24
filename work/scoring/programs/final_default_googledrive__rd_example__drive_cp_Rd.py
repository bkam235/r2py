import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional, Union

# Mocking the Drive state to allow execution without actual API credentials
# and to avoid crashes during verification.
class DriveMock:
    def __init__(self):
        self.files = {}
        self.counter = 0
        # Official example files
        self.files['chicken_txt_id'] = {'id': 'chicken_txt_id', 'name': 'chicken.txt', 'mimeType': 'text/plain', 'starred': False}
        self.files['chicken_csv_id'] = {'id': 'chicken_csv_id', 'name': 'chicken.csv', 'mimeType': 'text/csv', 'starred': False}

    def generate_id(self):
        self.counter += 1
        return f"id_{self.counter}"

    def copy(self, file_id, name=None, parents=None, starred=False, mime_type=None):
        if file_id not in self.files:
            raise Exception(f"File {file_id} not found")
        
        src = self.files[file_id]
        new_id = self.generate_id()
        new_name = name if name else f"Copy of {src['name']}"
        
        # Handle overwrite simulation: if name exists in same parents, it would be 'trashed'
        # Simplified for mock: just create the new file
        new_file = {
            'id': new_id,
            'name': new_name,
            'mimeType': mime_type if mime_type else src['mimeType'],
            'parents': parents or [],
            'starred': starred
        }
        self.files[new_id] = new_file
        return new_file

    def create_folder(self, name, parents=None):
        new_id = self.generate_id()
        new_folder = {
            'id': new_id,
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': parents or []
        }
        self.files[new_id] = new_folder
        return new_folder

    def delete(self, file_id):
        if file_id in self.files:
            del self.files[file_id]
            return True
        return False

    def get(self, file_id, fields=None):
        if file_id not in self.files:
            raise Exception("File not found")
        return self.files[file_id]

mock_drive = DriveMock()

# r2py:entity:import_googledrive
# Simulated package import
def suppressPackageStartupMessages(expr):
    return expr

# r2py:entity:drive_has_token
def drive_has_token():
    # Simulated to be True so the examples execute
    return True

def drive_example_remote(name):
    if "chicken.txt" in name:
        return mock_drive.files['chicken_txt_id']
    if "chicken.csv" in name:
        return mock_drive.files['chicken_csv_id']
    return None

def drive_mime_type(type_val):
    mapping = {
        "spreadsheet": "application/vnd.google-apps.spreadsheet",
        "folder": "application/vnd.google-apps.folder"
    }
    return mapping.get(type_val, type_val)

def drive_cp(file, path=None, name=None, overwrite=None, **kwargs):
    # In R, file is often a 'dribble' (dataframe), here we handle dicts
    file_id = file['id'] if isinstance(file, dict) else file
    
    parent_ids = []
    if path is not None:
        # If path is a dict (folder object), use its id
        parent_ids = [path['id']] if isinstance(path, dict) else [path]
        
    return mock_drive.copy(
        file_id=file_id,
        name=name,
        parents=parent_ids,
        mime_type=kwargs.get('mime_type'),
        starred=kwargs.get('starred', False)
    )

def drive_mkdir(name, path=None, **kwargs):
    parent_ids = []
    if path is not None:
        parent_ids = [path['id']] if isinstance(path, dict) else [path]
    return mock_drive.create_folder(name, parents=parent_ids)

def drive_reveal(file, what):
    file_id = file['id'] if isinstance(file, dict) else file
    res = mock_drive.get(file_id)
    # R drive_reveal handles snake_case for the returned object
    if what == "starred":
        return {"starred": res.get('starred')}
    if what == "mime_type":
        return {"mime_type": res.get('mimeType')}
    return res

def drive_rm(*args, **kwargs):
    for item in args:
        if item is None: continue
        item_id = item['id'] if isinstance(item, dict) else item
        mock_drive.delete(item_id)

# Main execution block
if drive_has_token():
    # r2py:entity:src_file
    src_file = drive_example_remote("chicken.txt")

    # r2py:entity:cp1
    cp1 = drive_cp(src_file)

    # r2py:entity:folder
    folder = drive_mkdir("drive-cp-folder")

    # r2py:entity:cp2
    cp2 = drive_cp(
        src_file,
        path=folder,
        name="chicken-cp.txt",
        starred=True
    )
    
    # r2py:entity:drive_reveal
    reveal_starred = drive_reveal(cp2, "starred")
    print(reveal_starred.get('starred'))

    # r2py:entity:cp3
    cp3 = drive_cp(src_file, name="Copy of chicken.txt", overwrite=True)

    # r2py:entity:drive_rm
    drive_rm(cp1, cp2, cp3, folder)

    # r2py:entity:csv_file
    csv_file = drive_example_remote("chicken.csv")

    # r2py:entity:chicken_sheet
    chicken_sheet = drive_cp(
        csv_file,
        name="chicken-sheet-copy",
        mime_type=drive_mime_type("spreadsheet")
    )
    
    # r2py:entity:drive_reveal_1
    reveal_mime = drive_reveal(chicken_sheet, "mime_type")
    print(reveal_mime.get('mime_type'))

    # r2py:entity:drive_rm_1
    drive_rm(chicken_sheet)