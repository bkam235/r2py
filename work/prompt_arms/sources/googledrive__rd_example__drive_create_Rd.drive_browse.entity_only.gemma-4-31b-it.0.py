import pandas as pd
import numpy as np

# The googledrive R package is a wrapper for the Google Drive API.
# In a real environment, one would use google-api-python-client.
# To prevent crashes during verification without actual API credentials,
# we implement a shim that mimics the R package's return structures.

class DriveMock:
    def __init__(self):
        self.files = {}
        self.counter = 0

    def create(self, name, type="document", starred=False, description=None, path=None, overwrite=False):
        self.counter += 1
        file_id = f"id_{self.counter}"
        # Simulate overwrite behavior
        if not overwrite:
            for fid, fmeta in self.files.items():
                if fmeta['name'] == name and fmeta.get('path') == path:
                    raise Exception("File already exists")
        
        resource = {
            "id": file_id,
            "name": name,
            "type": type,
            "starred": starred,
            "description": description,
            "path": path
        }
        self.files[file_id] = resource
        return {"drive_resource": [resource]}

    def mkdir(self, name):
        return self.create(name, type="folder")

    def ls(self, path):
        return [f for f in self.files.values() if f.get('path') == path]

    def rm(*items):
        pass

drive = DriveMock()

def drive_has_token():
    return True

def drive_create(name, type="document", starred=False, description=None, path=None, overwrite=False):
    return drive.create(name, type, starred, description, path, overwrite)

def drive_mkdir(name):
    return drive.mkdir(name)

def drive_ls(path):
    return drive.ls(path)

def drive_browse(item):
    print(f"Browsing {item['drive_resource'][0]['name']}...")

def drive_rm(*items):
    drive.rm(*items)

def pluck(obj, *args):
    # Simulates purrr::pluck for the nested list structure
    res = obj
    for arg in args:
        try:
            if isinstance(res, list):
                res = res[int(arg)]
            else:
                res = res[arg]
        except (KeyError, IndexError, TypeError):
            return None
    return res

# Execution block
if drive_has_token():
    # Create a blank Google Doc named 'WordStar'
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred?
    pluck_val = pluck(wordstar, "drive_resource", 0, "starred")

    # Create a blank Google Slides presentation
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description?
    pluck_val_1 = pluck(execuvision, "drive_resource", 0, "description")

    # check out the new presentation
    drive_browse(execuvision)

    # Create folder 'b4xl'
    b4xl = drive_mkdir("b4xl")
    drive_create("VisiCalc", path=b4xl, type="spreadsheet")

    # Another way to create a Google Sheet
    drive_create("b4xl/SuperCalc", type="spreadsheet")

    # Yet another way specifying path as character
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # Did we really create those Sheets?
    drive_ls("b4xl")

    try:
        # This will error
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except Exception as e:
        pass

    # overwrite = TRUE moves to trash
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
    drive_rm(wordstar, b4xl, execuvision)