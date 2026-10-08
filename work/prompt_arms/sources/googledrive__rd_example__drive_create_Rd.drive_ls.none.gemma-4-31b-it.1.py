import pandas as pd
import numpy as np

# Mocking googledrive and purrr functionality for execution equivalence
class DriveItem:
    def __init__(self, name, type_="file", starred=False, description=None, parents=None):
        self.name = name
        self.type = type_
        self.starred = starred
        self.description = description
        self.parents = parents or []
        self.id = f"id_{name}"
        self.drive_resource = [{'starred': starred, 'description': description}]

class GoogledriveMock:
    def __init__(self):
        self.files = {}

    def drive_has_token(self):
        return True

    def drive_create(self, name, type="file", starred=False, description=None, path=None, overwrite=False):
        # Simplified path handling
        parent_id = None
        if path:
            if isinstance(path, DriveItem):
                parent_id = path.id
            elif isinstance(path, str):
                # Handle "b4xl/SuperCalc" or "b4xl"
                folder_name = path.split('/')[0]
                for item in self.files.values():
                    if item.name == folder_name:
                        parent_id = item.id
                        break
        
        # Check overwrite
        existing = [f for f in self.files.values() if f.name == name and f.parents == [parent_id] if parent_id else False]
        if existing and not overwrite:
            raise RuntimeError("File already exists")
        
        # If overwrite is True and exists, we "trash" it (remove from dict)
        if existing and overwrite:
            for e in existing: del self.files[e.id]

        # Clean name if path was "b4xl/SuperCalc"
        final_name = name.split('/')[-1] if '/' in name else name
        item = DriveItem(final_name, type_=type, starred=starred, description=description, parents=[parent_id] if parent_id else [])
        self.files[item.id] = item
        return item

    def drive_mkdir(self, name):
        item = DriveItem(name, type_="folder")
        self.files[item.id] = item
        return item

    def drive_ls(self, path):
        parent_id = None
        if isinstance(path, str):
            for item in self.files.values():
                if item.name == path:
                    parent_id = item.id
                    break
        return [f for f in self.files.values() if parent_id in f.parents]

    def drive_browse(self, item):
        print(f"Browsing {item.name}...")

    def drive_rm(self, *items):
        for item in items:
            if item.id in self.files:
                del self.files[item.id]

gdrive = GoogledriveMock()
drive_has_token = gdrive.drive_has_token
drive_create = gdrive.drive_create
drive_mkdir = gdrive.drive_mkdir
drive_ls = gdrive.drive_ls
drive_browse = gdrive.drive_browse
drive_rm = gdrive.drive_rm

def pluck(obj, *args):
    # Mock purrr::pluck: dive into nested structures
    curr = obj
    for arg in args:
        if isinstance(curr, dict) and arg in curr:
            curr = curr[arg]
        elif isinstance(curr, list) and isinstance(arg, int) and arg < len(curr):
            curr = curr[arg]
        else:
            return None
    return curr

# --- Main Script ---
if drive_has_token():
    # Create a blank Google Doc named 'WordStar' in
    # your 'My Drive' root folder and star it
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred? YES
    starred_val = pluck(wordstar, "drive_resource", 0, "starred")

    # Create a blank Google Slides presentation in
    # the root folder, and set its description
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description? YES
    desc_val = pluck(execuvision, "drive_resource", 0, "description")

    # check out the new presentation
    drive_browse(execuvision)

    # Create folder 'b4xl' in the root folder,
    # then create an empty new Google Sheet in it
    b4xl = drive_mkdir("b4xl")
    drive_create("VisiCalc", path=b4xl, type="spreadsheet")

    # Another way to create a Google Sheet in the folder 'b4xl'
    drive_create("b4xl/SuperCalc", type="spreadsheet")

    # Yet another way to create a new file in a folder,
    # this time specifying parent `path` as a character
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # Did we really create those Sheets in the intended folder? YES
    ls_res = drive_ls("b4xl")

    # `overwrite = FALSE` errors if file already exists at target filepath
    # THIS WILL ERROR!
    try:
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except RuntimeError as e:
        pass # Expected error

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
    drive_rm(wordstar, b4xl, execuvision)