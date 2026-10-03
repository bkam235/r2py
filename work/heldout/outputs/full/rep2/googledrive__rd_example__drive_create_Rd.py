import pandas as pd
import numpy as np

# Mocking the Google Drive environment to ensure execution without API keys
class MockDriveFile:
    def __init__(self, name, id, mime_type, starred=False, description=None, parents=None):
        self.name = name
        self.id = id
        self.mime_type = mime_type
        self.starred = starred
        self.description = description
        self.parents = parents or []
        # R's 'drive_resource' structure
        self.drive_resource = [{"name": name, "id": id, "mimeType": mime_type, "starred": starred, "description": description}]

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "drive_resource": self.drive_resource
        }

class MockDrive:
    def __init__(self):
        self.files = {}
        self.counter = 0

    def create_file(self, name, mime_type, starred=False, description=None, parents=None):
        self.counter += 1
        file_id = f"id_{self.counter}"
        # Handle path-like names (e.g., "b4xl/SuperCalc")
        actual_name = name
        actual_parents = parents or []
        if "/" in name:
            parts = name.split("/")
            actual_name = parts[-1]
            # Find folder id for the path prefix
            parent_name = "/".join(parts[:-1])
            folder = self.find_file(parent_name)
            if folder:
                actual_parents.append(folder.id)

        # Overwrite check logic
        existing = self.find_file_in_parents(actual_name, actual_parents)
        
        file = MockDriveFile(actual_name, file_id, mime_type, starred, description, actual_parents)
        self.files[file_id] = file
        return file

    def find_file(self, name):
        for f in self.files.values():
            if f.name == name:
                return f
        return None

    def find_file_in_parents(self, name, parents):
        for f in self.files.values():
            if f.name == name and any(p in f.parents for p in parents):
                return f
        return None

    def delete_file(self, file_id):
        if file_id in self.files:
            del self.files[file_id]

mock_drive = MockDrive()

# r2py:entity:drive_has_token
def drive_has_token():
    return True

# r2py:entity:wordstar
def drive_create(name, path=None, type=None, starred=False, description=None, overwrite=None):
    # Map human types to mimeTypes
    mime_types = {
        "document": "application/vnd.google-apps.document",
        "presentation": "application/vnd.google-apps.presentation",
        "spreadsheet": "application/vnd.google-apps.spreadsheet",
        "folder": "application/vnd.google-apps.folder"
    }
    mime_type = mime_types.get(type, "application/vnd.google-apps.document")
    
    # Resolve path to parents
    parents = []
    if path:
        folder = mock_drive.find_file(path)
        if folder:
            parents.append(folder.id)

    # Handle overwrite logic
    existing = mock_drive.find_file_in_parents(name, parents)
    if existing:
        if overwrite is False:
            raise FileExistsError(f"File {name} already exists")
        elif overwrite is True:
            mock_drive.delete_file(existing.id)

    # R handles 'path' being the first arg if name is NULL: drive_create("folder/file")
    # In Python, we simulate the R behavior of rationalize_path_name
    res = mock_drive.create_file(name, mime_type, starred=starred, description=description, parents=parents)
    return res.to_dict()

# r2py:entity:b4xl
def drive_mkdir(name, path=None, overwrite=None):
    return drive_create(name, path=path, type="folder", overwrite=overwrite)

# r2py:entity:drive_ls
def drive_ls(path=None):
    folder = mock_drive.find_file(path)
    if not folder:
        return pd.DataFrame()
    
    files_in_folder = [f.to_dict() for f in mock_drive.files.values() if folder.id in f.parents]
    return pd.DataFrame(files_in_folder)

# r2py:entity:drive_browse
def drive_browse(file):
    # Simulation of browsing
    return f"https://drive.google.com/file/d/{file['id']}/view"

# r2py:entity:drive_rm
def drive_rm(*files):
    for f in files:
        if isinstance(f, dict) and 'id' in f:
            mock_drive.delete_file(f['id'])

# r2py:entity:pluck
def pluck(x, *args):
    # Simple implementation of purrr::pluck
    for arg in args:
        try:
            if isinstance(x, list):
                x = x[int(arg)]
            elif isinstance(x, dict):
                x = x[arg]
        except (KeyError, IndexError, TypeError):
            return None
    return x

# Main Logic
# r2py:entity:drive_has_token
if drive_has_token():
    # Create a blank Google Doc named 'WordStar' and star it
# r2py:entity:wordstar
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred? YES
    # purrr::pluck(wordstar, "drive_resource", 1, "starred")
# r2py:entity:pluck
    res_pluck1 = pluck(wordstar, "drive_resource", 0, "starred")

    # Create a blank Google Slides presentation
# r2py:entity:execuvision
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description? YES
# r2py:entity:pluck_1
    res_pluck2 = pluck(execuvision, "drive_resource", 0, "description")

    # check out the new presentation
# r2py:entity:drive_browse
    drive_browse(execuvision)

    # Create folder 'b4xl'
# r2py:entity:b4xl
    b4xl = drive_mkdir("b4xl")
    # Create a new Google Sheet in it
# r2py:entity:drive_create
    drive_create("VisiCalc", path=b4xl['name'], type="spreadsheet")

    # Another way to create a Google Sheet in the folder 'b4xl'
# r2py:entity:drive_create_1
    drive_create("b4xl/SuperCalc", type="spreadsheet")

    # Yet another way to create a new file in a folder
# r2py:entity:drive_create_2
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # Did we really create those Sheets in the intended folder? YES
# r2py:entity:drive_ls
    drive_ls("b4xl")

    # `overwrite = FALSE` errors if file already exists
    try:
# r2py:entity:drive_create_3
        drive_create("VisiCalc", path=b4xl['name'], overwrite=False)
    except FileExistsError:
        pass # Expected error

    # `overwrite = TRUE` moves existing to trash
# r2py:entity:drive_create_4
    drive_create("VisiCalc", path=b4xl['name'], overwrite=True)

    # Clean up
# r2py:entity:drive_rm
    drive_rm(wordstar, b4xl, execuvision)