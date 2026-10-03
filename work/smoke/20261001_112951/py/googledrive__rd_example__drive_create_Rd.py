import pandas as pd
import numpy as np

# Mocking the googledrive package behavior for execution equivalence
# r2py:entity:wordstar
class DriveFile:
    def __init__(self, name, id, mime_type, starred=False, description=None, parents=None):
        self.name = name
        self.id = id
        self.mime_type = mime_type
        self.starred = starred
        self.description = description
        self.parents = parents or []
        self.drive_resource = [{"name": name, "id": id, "mimeType": mime_type, "starred": starred, "description": description}]

    def get(self, key):
        return getattr(self, key, None)

class MockDriveService:
    def __init__(self):
        self.files = []
        self.token_exists = True  # Simulate drive_has_token()

    def create_file(self, name, type=None, starred=False, description=None, path=None, overwrite=None):
        # Handle MIME types
        mime_map = {
            "document": "application/vnd.google-apps.document",
            "presentation": "application/vnd.google-apps.presentation",
            "spreadsheet": "application/vnd.google-apps.spreadsheet",
            "folder": "application/vnd.google-apps.folder"
        }
        mime_type = mime_map.get(type, type)

        # Handle path/parents
        parent_ids = []
        if path:
            if isinstance(path, DriveFile):
                parent_ids = [path.id]
            elif isinstance(path, str):
                # Check if path is a composite "folder/file"
                if "/" in path:
                    folder_name, name = path.split("/", 1)
                    folder = next((f for f in self.files if f.name == folder_name), None)
                    if folder: parent_ids = [folder.id]
                else:
                    folder = next((f for f in self.files if f.name == path), None)
                    if folder: parent_ids = [folder.id]

        # Overwrite logic
        existing = [f for f in self.files if f.name == name and f.parents == parent_ids]
        if existing:
            if overwrite is False:
                raise FileExistsError(f"File {name} already exists")
            elif overwrite is True:
                for e in existing:
                    self.files.remove(e)

        new_file = DriveFile(name, f"id_{len(self.files)}", mime_type, starred, description, parent_ids)
        self.files.append(new_file)
        return new_file

    def list_files(self, path=None):
        if path is None:
            return self.files
        if isinstance(path, str):
            folder = next((f for f in self.files if f.name == path), None)
            if folder:
                return [f for f in self.files if folder.id in f.parents]
        if isinstance(path, DriveFile):
            return [f for f in self.files if path.id in f.parents]
        return []

    def delete_files(self, *files):
        for f in files:
            if f in self.files:
                self.files.remove(f)

service = MockDriveService()

# r2py:entity:drive_has_token
def drive_has_token():
    return service.token_exists

def drive_create(name, type=None, starred=False, description=None, path=None, overwrite=None):
    return service.create_file(name, type, starred, description, path, overwrite)

# r2py:entity:b4xl
def drive_mkdir(name, path=None, overwrite=None):
    return drive_create(name, type="folder", path=path, overwrite=overwrite)

# r2py:entity:drive_ls
def drive_ls(path=None):
    return service.list_files(path)

# r2py:entity:drive_browse
def drive_browse(file):
    # In R, this opens a browser. In Python, we simulate by printing.
    print(f"Browsing file: {file.name}")
    return file

# r2py:entity:drive_rm
def drive_rm(*files):
    service.delete_files(*files)

# r2py:entity:pluck
def pluck(obj, *keys):
    # R purrr::pluck(wordstar, "drive_resource", 1, "starred")
    curr = obj
    for key in keys:
        if isinstance(curr, list):
            curr = curr[int(key) - 1] if isinstance(key, (int, str)) and str(key).isdigit() else curr.get(key)
        elif isinstance(curr, dict):
            curr = curr.get(key)
        else:
            # Handle the specific structure of our DriveFile object
            if hasattr(curr, 'drive_resource') and key == "drive_resource":
                curr = curr.drive_resource
            elif isinstance(curr, list) and key == "drive_resource":
                # In the R version, the result is often a list of resources
                curr = [f.drive_resource for f in curr]
            else:
                try:
                    curr = curr[key]
                except:
                    return None
    return curr

# r2py:entity:drive_has_token
if drive_has_token():
    # Create a blank Google Doc named 'WordStar' in your 'My Drive' root folder and star it
# r2py:entity:wordstar
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred? YES
# r2py:entity:pluck
    pluck_val = pluck(wordstar, "drive_resource", 1, "starred")

    # Create a blank Google Slides presentation in the root folder, and set its description
# r2py:entity:execuvision
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description? YES
# r2py:entity:pluck_1
    pluck_val_2 = pluck(execuvision, "drive_resource", 1, "description")

    # check out the new presentation
# r2py:entity:drive_browse
    drive_browse(execuvision)

    # Create folder 'b4xl' in the root folder, then create an empty new Google Sheet in it
# r2py:entity:b4xl
    b4xl = drive_mkdir("b4xl")
# r2py:entity:drive_create
    drive_create("VisiCalc", path=b4xl, type="spreadsheet")

    # Another way to create a Google Sheet in the folder 'b4xl'
# r2py:entity:drive_create_1
    drive_create("b4xl/SuperCalc", type="spreadsheet")

    # Yet another way to create a new file in a folder, this time specifying parent `path` as a character
# r2py:entity:drive_create_2
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # Did we really create those Sheets in the intended folder? YES
# r2py:entity:drive_ls
    drive_ls("b4xl")

    # `overwrite = FALSE` errors if file already exists at target filepath
    try:
# r2py:entity:drive_create_3
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except FileExistsError:
        pass # This is the expected behavior

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
# r2py:entity:drive_create_4
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
# r2py:entity:drive_rm
    drive_rm(wordstar, b4xl, execuvision)