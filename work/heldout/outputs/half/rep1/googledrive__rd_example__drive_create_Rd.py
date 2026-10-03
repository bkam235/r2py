import pandas as pd
import numpy as np

# Mocking the googledrive package behavior
class MockDriveFile:
    def __init__(self, name, mime_type, starred=False, description=None, parents=None):
        self.id = f"id_{name}"
        self.name = name
        self.mime_type = mime_type
        self.starred = starred
        self.description = description
        self.parents = parents or []
        self.webViewLink = f"https://drive.google.com/file/d/{self.id}/view"
        self.kind = "drive#file"

class MockDriveState:
    def __init__(self):
        self.files = {}
    
    def create_file(self, name, mime_type, starred=False, description=None, parents=None, overwrite=None):
        if name is None:
            return None
            
        existing = [f for f in self.files.values() if f.name == name and f.parents == parents]
        
        if existing:
            if overwrite is False:
                raise RuntimeError(f"File {name} already exists")
            if overwrite is True:
                for f in existing:
                    del self.files[f.id]
        
        new_file = MockDriveFile(name, mime_type, starred, description, parents)
        self.files[new_file.id] = new_file
        return new_file

    def delete_file(self, file_id):
        if file_id in self.files:
            del self.files[file_id]
            return True
        return False

    def list_files(self, parents=None):
        if parents is None:
            return list(self.files.values())
        return [f for f in self.files.values() if parents in f.parents]

# Global state to simulate the Google Drive
_state = MockDriveState()

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
    parent_id = None
    final_name = name
    
    if path is not None:
        if isinstance(path, dict):
            parent_id = path["id"][0]
        elif isinstance(path, str):
            if "/" in path:
                parts = path.split("/")
                folder = next((f for f in _state.files.values() if f.name == parts[0]), None)
                if folder:
                    parent_id = folder.id
                    final_name = parts[1]
            else:
                folder = next((f for f in _state.files.values() if f.name == path), None)
                if folder:
                    parent_id = folder.id
        
    parents = [parent_id] if parent_id else []
    res = _state.create_file(final_name, mime, starred=starred, description=description, parents=parents, overwrite=overwrite)
    
    return {
        "name": [res.name],
        "id": [res.id],
        "drive_resource": [res]
    }

# r2py:entity:b4xl
def drive_mkdir(name, path=None, overwrite=None):
    return drive_create(name, path=path, type="folder", overwrite=overwrite)

# r2py:entity:drive_ls
def drive_ls(path=None):
    parent_id = None
    if isinstance(path, str):
        folder = next((f for f in _state.files.values() if f.name == path), None)
        if folder:
            parent_id = folder.id
    elif isinstance(path, dict):
        parent_id = path["id"][0]
        
    files = _state.list_files(parents=parent_id)
    return pd.DataFrame([{"name": f.name, "id": f.id} for f in files])

# r2py:entity:drive_browse
def drive_browse(file):
    res = file["drive_resource"][0]
    # drive_browse in R opens a browser; here we mimic the side effect
    # but we don't print it if it's not the final value in R's autoprint context.
    # However, for translation, we keep it as a silent action.
    pass

# r2py:entity:drive_rm
def drive_rm(*args):
    for arg in args:
        if isinstance(arg, dict):
            fid = arg["id"][0]
            _state.delete_file(fid)

# r2py:entity:pluck
def pluck(x, *args):
    val = x
    for key in args:
        if isinstance(val, list):
            val = val[key]
        elif isinstance(val, dict):
            val = val.get(key)
        else:
            val = getattr(val, key, None)
    return val

# Main execution block
if drive_has_token():
    # Create a blank Google Doc named 'WordStar'
# r2py:entity:wordstar
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred? (Silent in R examples)
# r2py:entity:pluck
    pluck(wordstar, "drive_resource", 0, "starred")

    # Create a blank Google Slides presentation
# r2py:entity:execuvision
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description? (Silent in R examples)
# r2py:entity:pluck_1
    pluck(execuvision, "drive_resource", 0, "description")

    # check out the new presentation
# r2py:entity:drive_browse
    drive_browse(execuvision)

    # Create folder 'b4xl'
# r2py:entity:b4xl
    b4xl = drive_mkdir("b4xl")
# r2py:entity:drive_create
    drive_create("VisiCalc", path=b4xl, type="spreadsheet")

    # Another way to create a Google Sheet in the folder 'b4xl'
# r2py:entity:drive_create_1
    drive_create("b4xl/SuperCalc", type="spreadsheet")

    # Yet another way specifying parent `path` as a character
# r2py:entity:drive_create_2
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # Did we really create those Sheets in the intended folder?
# r2py:entity:drive_ls
    drive_ls("b4xl")

    # `overwrite = FALSE` errors if file already exists
    try:
# r2py:entity:drive_create_3
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except RuntimeError:
        pass

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
# r2py:entity:drive_create_4
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
# r2py:entity:drive_rm
    drive_rm(wordstar, b4xl, execuvision)