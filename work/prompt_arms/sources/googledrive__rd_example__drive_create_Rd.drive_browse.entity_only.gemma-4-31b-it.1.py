import pandas as pd
import numpy as np

# Mocking googledrive behavior since actual API authentication is not possible in this environment
# and the R code is essentially demonstrating API calls.

class MockDriveResource:
    def __init__(self, name, type_val, starred=False, description=None):
        self.name = name
        self.type = type_val
        self.starred = starred
        self.description = description
        self.id = f"id_{name}"

    def __getitem__(self, key):
        if key == "drive_resource":
            return [self]
        return getattr(self, key)

def drive_has_token():
    return True

def drive_create(name, type="document", starred=False, description=None, path=None, overwrite=False):
    # Simulating the R function's behavior
    if not overwrite and name == "VisiCalc" and path is not None:
        # In the R script, this specific call is marked "THIS WILL ERROR!"
        raise RuntimeError("File already exists")
    
    # Map R types to mock types
    return MockDriveResource(name, type, starred=starred, description=description)

def drive_mkdir(name):
    return MockDriveResource(name, "folder")

def drive_browse(resource):
    print(f"Browsing {resource.name}...")
    return None

def drive_ls(path):
    print(f"Listing contents of {path}...
    VisiCalc
    SuperCalc
    Lotus 1-2-3")
    return None

def drive_rm(*args):
    print(f"Removing {args}...")
    return None

def pluck(obj, key, index, subkey):
    # Mimicking purrr::pluck(wordstar, "drive_resource", 1, "starred")
    # Note: R uses 1-based indexing, Python uses 0-based
    try:
        res = obj[key][index-1]
        return getattr(res, subkey)
    except:
        return None

# Start of translated R logic
if drive_has_token():
    # Create a blank Google Doc named 'WordStar'
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred? YES
    starred_status = pluck(wordstar, "drive_resource", 1, "starred")

    # Create a blank Google Slides presentation
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description? YES
    desc_status = pluck(execuvision, "drive_resource", 1, "description")

    # check out the new presentation
    drive_browse(execuvision)

    # Create folder 'b4xl'
    b4xl = drive_mkdir("b4xl")
    drive_create("VisiCalc", path=b4xl, type="spreadsheet")

    # Another way to create a Google Sheet
    drive_create("b4xl/SuperCalc", type="spreadsheet")

    # Yet another way to create a new file
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # Did we really create those Sheets in the intended folder? YES
    drive_ls("b4xl")

    # `overwrite = FALSE` errors if file already exists
    try:
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except RuntimeError as e:
        print(f"Caught expected error: {e}")

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
    drive_rm(wordstar, b4xl, execuvision)