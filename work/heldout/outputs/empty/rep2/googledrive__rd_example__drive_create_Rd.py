import pandas as pd
import numpy as np

# Mocking the Google Drive API to ensure execution equivalence without real API keys
class MockDriveFile:
    def __init__(self, id, name, mimeType, starred=False, description=None):
        self.id = id
        self.name = name
        self.mimeType = mimeType
        self.starred = starred
        self.description = description
        self.parents = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "mimeType": self.mimeType,
            "starred": self.starred,
            "description": self.description,
            "parents": self.parents,
            "webViewLink": f"https://drive.google.com/file/d/{self.id}/view"
        }

class MockDriveService:
    def __init__(self):
        self.files = []
        self.counter = 0

    def _generate_id(self):
        self.counter += 1
        return f"id_{self.counter}"

    def create_file(self, name, mimeType, starred=False, description=None, parents=None, overwrite=None):
        # Handle path/parents
        parent_id = None
        if parents:
            parent_id = parents[0]

        # Check for existing file (overwrite logic)
        existing = next((f for f in self.files if f.name == name and (not parent_id or f.parents == [parent_id])), None)
        
        if existing:
            if overwrite is False:
                raise RuntimeError(f"File {name} already exists")
            if overwrite is True:
                # Move to trash (simulated by removing from active files)
                self.files.remove(existing)

        new_file = MockDriveFile(self._generate_id(), name, mimeType, starred, description)
        if parent_id:
            new_file.parents = [parent_id]
        self.files.append(new_file)
        return new_file

    def list_files(self, q=None):
        # Simplified query simulation
        return [f.to_dict() for f in self.files]

    def delete_file(self, id):
        self.files = [f for f in self.files if f.id != id]

drive_service = MockDriveService()

# R-like dribble: a dataframe with a 'drive_resource' column containing the API response
def as_dribble(files_list):
    if not files_list:
        return pd.DataFrame(columns=["name", "id", "drive_resource"])
    
    data = []
    for f in files_list:
        res = f.to_dict() if isinstance(f, MockDriveFile) else f
        data.append({
            "name": res["name"],
            "id": res["id"],
            "drive_resource": res
        })
    return pd.DataFrame(data)

# r2py:entity:drive_has_token
def drive_has_token():
    return True

def drive_create(name, path=None, type=None, starred=False, description=None, overwrite=None):
    mime_types = {
        "document": "application/vnd.google-apps.document",
        "presentation": "application/vnd.google-apps.presentation",
        "spreadsheet": "application/vnd.google-apps.spreadsheet",
        "folder": "application/vnd.google-apps.folder"
    }
    mime_type = mime_types.get(type, "application/vnd.google-apps.document")
    
    # Handle path as a folder object or string
    parent_id = None
    if path is not None:
        if isinstance(path, pd.DataFrame):
            parent_id = path.iloc[0]["id"]
        elif isinstance(path, str):
            # Handle "folder/file" syntax
            if "/" in name:
                parts = name.split("/", 1)
                folder_name = parts[0]
                name = parts[1]
                folder = next((f for f in drive_service.files if f.name == folder_name), None)
                if folder: parent_id = folder.id
            else:
                folder = next((f for f in drive_service.files if f.name == path), None)
                if folder: parent_id = folder.id
    
    parents = [parent_id] if parent_id else None
    file_obj = drive_service.create_file(
        name=name, 
        mimeType=mime_type, 
        starred=starred, 
        description=description, 
        parents=parents, 
        overwrite=overwrite
    )
    return as_dribble([file_obj])

def drive_mkdir(name, path=None, overwrite=None):
    return drive_create(name=name, path=path, type="folder", overwrite=overwrite)

def drive_ls(path=None):
    if path is None:
        return as_dribble(drive_service.list_files())
    
    # Find folder id
    folder = next((f for f in drive_service.files if f.name == path), None)
    if not folder:
        return as_dribble([])
    
    children = [f for f in drive_service.files if folder.id in f.parents]
    return as_dribble(children)

def drive_rm(*files):
    for f in files:
        if isinstance(f, pd.DataFrame):
            file_id = f.iloc[0]["id"]
            drive_service.delete_file(file_id)

def drive_browse(file):
    link = file.iloc[0]["drive_resource"]["webViewLink"]
    # R's drive_browse often returns links invisibly and calls browseURL. 
    # In a non-interactive environment, it typically produces no stdout.
    return link

def pluck(dribble, key, idx, subkey):
    # mimics purrr::pluck(wordstar, "drive_resource", 1, "starred")
    resource = dribble.iloc[0]["drive_resource"]
    return resource.get(subkey)

# --- Main Execution ---

# wordstar <- drive_create("WordStar", type = "document", starred = TRUE)
# r2py:entity:wordstar
wordstar = drive_create("WordStar", type="document", starred=True)

# purrr::pluck(wordstar, "drive_resource", 1, "starred")
# r2py:entity:pluck
starred_val = pluck(wordstar, "drive_resource", 1, "starred")

# execuvision <- drive_create(...)
# r2py:entity:execuvision
execuvision = drive_create(
    "ExecuVision",
    type="presentation",
    description="deeply nested bullet lists FTW"
)

# purrr::pluck(execuvision, "drive_resource", 1, "description")
# r2py:entity:pluck_1
desc_val = pluck(execuvision, "drive_resource", 1, "description")

# drive_browse(execuvision)
# r2py:entity:drive_browse
drive_browse(execuvision)

# b4xl <- drive_mkdir("b4xl")
# r2py:entity:b4xl
b4xl = drive_mkdir("b4xl")

# drive_create("VisiCalc", path = b4xl, type = "spreadsheet")
# r2py:entity:drive_create
drive_create("VisiCalc", path=b4xl, type="spreadsheet")

# Another way: drive_create("b4xl/SuperCalc", type = "spreadsheet")
# r2py:entity:drive_create_1
drive_create("b4xl/SuperCalc", type="spreadsheet")

# Yet another: drive_create("Lotus 1-2-3", path = "b4xl", type = "spreadsheet")
# r2py:entity:drive_create_2
drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

# drive_ls("b4xl")
# r2py:entity:drive_ls
drive_ls("b4xl")

# `overwrite = FALSE` errors if file already exists
# r2py:entity:drive_create_3
try:
    drive_create("VisiCalc", path=b4xl, overwrite=False)
except RuntimeError:
    pass

# `overwrite = TRUE` moves an existing file to trash, then proceeds
# r2py:entity:drive_create_4
drive_create("VisiCalc", path=b4xl, overwrite=True)

# Clean up
# r2py:entity:drive_rm
drive_rm(wordstar, b4xl, execuvision)