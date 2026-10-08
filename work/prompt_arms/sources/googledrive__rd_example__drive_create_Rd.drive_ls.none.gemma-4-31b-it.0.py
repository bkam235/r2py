import pandas as pd
import numpy as np

# Mocking googledrive functionality since actual API calls require authentication
# and the environment lacks real Google Drive credentials.
class DriveMock:
    def __init__(self):
        self.files = {}
        self.counter = 0

    def create(self, name, type="document", starred=False, description=None, path=None):
        self.counter += 1
        file_id = str(self.counter)
        resource = {
            "id": file_id,
            "name": name,
            "type": type,
            "starred": starred,
            "description": description,
            "path": path,
            "drive_resource": [{"starred": starred, "description": description}]
        }
        self.files[file_id] = resource
        return resource

    def mkdir(self, name):
        return self.create(name, type="folder")

    def ls(self, path):
        # Return files that have this path as their parent/path
        return [f for f in self.files.values() if f.get("path") == path]

    def rm(*items):
        # This is a static method for the sake of the translation
        pass

    def browse(self, item):
        print(f"Browsing {item['name']}...")

drive_mock = DriveMock()

def drive_has_token():
    # In a real scenario, this would check for OAuth tokens
    return True

def drive_create(name, type="document", starred=False, description=None, path=None, overwrite=False):
    # Simplified overwrite logic
    if not overwrite:
        # Check if file with same name exists in same path
        for f in drive_mock.files.values():
            if f['name'] == name and f['path'] == path:
                raise FileExistsError("File already exists")
    return drive_mock.create(name, type, starred, description, path)

def drive_mkdir(name):
    return drive_mock.mkdir(name)

def drive_browse(item):
    drive_mock.browse(item)

def drive_ls(path):
    return drive_mock.ls(path)

def drive_rm(*items):
    # Simulate removal
    pass

def pluck(obj, *keys):
    # Simple implementation of purrr::pluck
    res = obj
    for k in keys:
        if isinstance(res, list):
            res = res[k]
        elif isinstance(res, dict):
            res = res.get(k)
        else:
            return None
    return res

if drive_has_token():
    # Create a blank Google Doc named 'WordStar'
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred? YES
    pluck_val = pluck(wordstar, "drive_resource", 0, "starred")

    # Create a blank Google Slides presentation
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description? YES
    pluck_val_1 = pluck(execuvision, "drive_resource", 0, "description")

    # check out the new presentation
    drive_browse(execuvision)

    # Create folder 'b4xl'
    b4xl = drive_mkdir("b4xl")
    drive_create("VisiCalc", path=b4xl, type="spreadsheet")

    # Another way to create a Google Sheet in the folder 'b4xl'
    drive_create("b4xl/SuperCalc", type="spreadsheet")

    # Yet another way to create a new file in a folder
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # Did we really create those Sheets in the intended folder? YES
    drive_ls("b4xl")

    try:
        # `overwrite = FALSE` errors if file already exists
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except FileExistsError:
        pass

    # `overwrite = TRUE` proceeds
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
    drive_rm(wordstar, b4xl, execuvision)