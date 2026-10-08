import pandas as pd
import numpy as np

class MockDriveResource:
    def __init__(self, name, type="document", starred=False, description=None, path=None):
        self.name = name
        self.type = type
        self.starred = starred
        self.description = description
        self.path = path
        self.id = f"id_{name}"
        self.drive_resource = [{"starred": starred, "description": description}]

class MockDrive:
    def __init__(self):
        self.files = {}

    def create(self, name, type="document", starred=False, description=None, path=None, overwrite=False):
        if not overwrite:
            for f in self.files.values():
                if f.name == name and f.path == path:
                    raise FileExistsError("File already exists")
        
        res = MockDriveResource(name, type, starred, description, path)
        self.files[res.id] = res
        return res

    def mkdir(self, name):
        return self.create(name, type="folder")

    def ls(self, path):
        return [f for f in self.files.values() if f.path == path]

    def rm(self, *items):
        for item in items:
            if hasattr(item, 'id'):
                self.files.pop(item.id, None)

drive = MockDrive()

def drive_has_token():
    return True

def drive_create(name, type="document", starred=False, description=None, path=None, overwrite=False):
    # Handle path as "folder/file"
    if "/" in name:
        path, name = name.split("/", 1)
    return drive.create(name, type, starred, description, path, overwrite)

def drive_mkdir(name):
    return drive.mkdir(name)

def drive_ls(path):
    return drive.ls(path)

def drive_browse(item):
    pass

def drive_rm(*items):
    drive.rm(*items)

def pluck(obj, *keys):
    val = obj
    for key in keys:
        if isinstance(val, list):
            val = val[key]
        elif isinstance(val, dict):
            val = val.get(key)
        else:
            val = getattr(val, key, None)
    return val

# Main execution
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

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
    drive_rm(wordstar, b4xl, execuvision)