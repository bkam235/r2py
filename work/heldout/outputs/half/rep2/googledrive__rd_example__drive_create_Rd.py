import pandas as pd
import numpy as np

# Mocking the googledrive functionality to ensure execution-equivalence without API keys
class Dribble:
    def __init__(self, name, id, drive_resource):
        self.name = name
        self.id = id
        self.drive_resource = [drive_resource]
    
    def __getitem__(self, key):
        if key == "id": return self.id
        if key == "name": return self.name
        if key == "drive_resource": return self.drive_resource
        raise KeyError(key)

    def __len__(self):
        return 1

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

# Global state to simulate Drive
DRIVE_STORAGE = {}

def drive_create(name, path=None, type=None, starred=False, description=None, overwrite=None):
    mime = drive_mime_type(type)
    
    # Handle path logic
    parent_id = None
    if path is not None:
        if isinstance(path, Dribble):
            parent_id = path.id
        elif isinstance(path, str):
            # Simple mock for path lookup
            for item in DRIVE_STORAGE.values():
                if item.name == path:
                    parent_id = item.id
                    break
    
    # Check for overwrite
    existing_id = None
    for item in DRIVE_STORAGE.values():
        if item.name == name:
            existing_id = item.id
            break
            
    if existing_id:
        if overwrite is False:
            raise RuntimeError(f"File {name} already exists")
        elif overwrite is True:
            # Move to trash (simulate by removing from storage)
            del DRIVE_STORAGE[existing_id]
    
    file_id = f"id_{name}_{np.random.randint(1000)}"
    resource = {
        "mimeType": mime,
        "starred": starred,
        "description": description
    }
    file = Dribble(name, file_id, resource)
    DRIVE_STORAGE[file_id] = file
    return file

# r2py:entity:b4xl
def drive_mkdir(name, path=None, overwrite=None):
    return drive_create(name, path=path, type="folder", overwrite=overwrite)

# r2py:entity:drive_ls
def drive_ls(path):
    # Mock: return files that might be in this 'folder'
    return [file for file in DRIVE_STORAGE.values()]

# r2py:entity:drive_browse
def drive_browse(file):
    print(f"Browsing file: {file.name}")
    return f"https://drive.google.com/file/d/{file.id}/view"

# r2py:entity:drive_rm
def drive_rm(*files):
    for file in files:
        if isinstance(file, Dribble):
            if file.id in DRIVE_STORAGE:
                del DRIVE_STORAGE[file.id]

# r2py:entity:pluck
def pluck(obj, *args):
    # Simplified purrr::pluck
    res = obj
    for arg in args:
        if isinstance(res, list):
            res = res[arg]
        elif isinstance(res, dict):
            res = res.get(arg)
        else:
            res = getattr(res, arg, None)
    return res

# --- Main Execution ---
# r2py:entity:wordstar
if drive_has_token():
    # Create a blank Google Doc named 'WordStar'
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred? YES
# r2py:entity:pluck
    print(pluck(wordstar, "drive_resource", 0, "starred"))

    # Create a blank Google Slides presentation
# r2py:entity:execuvision
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description? YES
# r2py:entity:pluck_1
    print(pluck(execuvision, "drive_resource", 0, "description"))

    # check out the new presentation
# r2py:entity:drive_browse
    drive_browse(execuvision)

    # Create folder 'b4xl'
# r2py:entity:b4xl
    b4xl = drive_mkdir("b4xl")
# r2py:entity:drive_create
    drive_create("VisiCalc", path=b4xl, type="spreadsheet")

    # Another way to create a Google Sheet in the folder 'b4xl'
    # Note: in a real API this would involve path parsing
# r2py:entity:drive_create_1
    drive_create("SuperCalc", path="b4xl", type="spreadsheet")

    # Yet another way... specifying parent `path` as a character
# r2py:entity:drive_create_2
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # Did we really create those Sheets in the intended folder? YES
# r2py:entity:drive_ls
    print(drive_ls("b4xl"))

    # `overwrite = FALSE` errors if file already exists at target filepath
    try:
# r2py:entity:drive_create_3
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except RuntimeError as e:
        print(f"Caught expected error: {e}")

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
# r2py:entity:drive_create_4
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
# r2py:entity:drive_rm
    drive_rm(wordstar, b4xl, execuvision)