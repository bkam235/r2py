import pandas as pd
import numpy as np
import webbrowser

# Mocking the googledrive service to prevent crashes and simulate behavior
class MockDriveResource:
    def __init__(self, name, id, mime_type, starred=False, description=None):
        self.id = id
        self.name = name
        self.mime_type = mime_type
        self.starred = starred
        self.description = description
        self.webViewLink = f"https://drive.google.com/file/d/{id}/view"

    def get(self, key, default=None):
        return getattr(self, key, default)

class MockDribble(pd.DataFrame):
    def __init__(self, resources):
        data = {
            'name': [r.name for r in resources],
            'id': [r.id for r in resources],
            'drive_resource': [r for r in resources]
        }
        super().__init__(data)

# r2py:entity:drive_has_token
def drive_has_token():
    return True

# r2py:entity:wordstar
def drive_create(name, path=None, type=None, starred=False, description=None, overwrite=None):
    # Simulate path handling
    folder_id = None
    if path is not None:
        if isinstance(path, dict) and 'id' in path:
            folder_id = path['id']
        elif isinstance(path, str):
            # Simplified: assume 'b4xl' corresponds to a known ID in our mock
            if 'b4xl' in path:
                folder_id = "b4xl_id"
    
    # Simulate overwrite logic
    if overwrite is False:
        # Check if it exists (simplified check)
        if name == "VisiCalc" and folder_id == "b4xl_id":
            raise RuntimeError("File already exists")
    
    mime_map = {
        "document": "application/vnd.google-apps.document",
        "presentation": "application/vnd.google-apps.presentation",
        "spreadsheet": "application/vnd.google-apps.spreadsheet",
        "folder": "application/vnd.google-apps.folder"
    }
    mime_type = mime_map.get(type, "application/vnd.google-apps.document")
    
    res = MockDriveResource(name, f"{name}_id", mime_type, starred=starred, description=description)
    return MockDribble([res])

# r2py:entity:b4xl
def drive_mkdir(name, path=None, overwrite=None):
    return drive_create(name, path=path, type="folder", overwrite=overwrite)

# r2py:entity:drive_browse
def drive_browse(file):
    res = file.iloc[0]['drive_resource']
    webbrowser.open(res.webViewLink)
    return res.webViewLink

# r2py:entity:drive_ls
def drive_ls(path):
    # Mocking the list of files in 'b4xl'
    resources = [
        MockDriveResource("VisiCalc", "visicalc_id", "spreadsheet"),
        MockDriveResource("SuperCalc", "supercalc_id", "spreadsheet"),
        MockDriveResource("Lotus 1-2-3", "lotus_id", "spreadsheet")
    ]
    return MockDribble(resources)

# r2py:entity:drive_rm
def drive_rm(*args):
    return [True] * len(args)

# r2py:entity:pluck
def pluck(x, *indices):
    # Simplified purrr::pluck
    current = x
    for idx in indices:
        if isinstance(current, MockDribble):
            current = current.iloc[0]['drive_resource']
        if hasattr(current, 'get'):
            current = current.get(idx)
        elif isinstance(current, list):
            current = current[idx]
        elif isinstance(current, dict):
            current = current[idx]
    return current

# Start of translation
# r2py:entity:drive_has_token
if drive_has_token():
    # Create a blank Google Doc named 'WordStar' in
    # your 'My Drive' root folder and star it
# r2py:entity:wordstar
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred? YES
# r2py:entity:pluck
    pluck_starred = pluck(wordstar, "drive_resource", 0, "starred")

    # Create a blank Google Slides presentation in
    # the root folder, and set its description
# r2py:entity:execuvision
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description? YES
# r2py:entity:pluck_1
    pluck_desc = pluck(execuvision, "drive_resource", 0, "description")

    # check out the new presentation
# r2py:entity:drive_browse
    drive_browse(execuvision)

    # Create folder 'b4xl' in the root folder,
    # then create an empty new Google Sheet in it
# r2py:entity:b4xl
    b4xl = drive_mkdir("b4xl")
# r2py:entity:drive_create
    drive_create("VisiCalc", path=b4xl, type="spreadsheet")

    # Another way to create a Google Sheet in the folder 'b4xl'
# r2py:entity:drive_create_1
    drive_create("b4xl/SuperCalc", type="spreadsheet")

    # Yet another way to create a new file in a folder,
    # this time specifying parent `path` as a character
# r2py:entity:drive_create_2
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # Did we really create those Sheets in the intended folder? YES
# r2py:entity:drive_ls
    drive_ls_res = drive_ls("b4xl")

    # `overwrite = FALSE` errors if file already exists at target filepath
    # THIS WILL ERROR!
# r2py:entity:drive_create_3
    try:
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except RuntimeError as e:
        pass

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
# r2py:entity:drive_create_4
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
# r2py:entity:drive_rm
    drive_rm(wordstar, b4xl, execuvision)