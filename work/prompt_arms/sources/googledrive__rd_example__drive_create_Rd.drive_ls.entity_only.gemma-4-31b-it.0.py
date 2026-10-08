import pandas as pd
import numpy as np

# Mocking the googledrive behavior to allow execution without API keys
class DriveResource:
    def __init__(self, name, type="document", starred=False, description=None):
        self.name = name
        self.type = type
        self.starred = starred
        self.description = description
        self.id = "mock_id_" + name
        self.drive_resource = [{"starred": starred, "description": description}]

def drive_has_token():
    return True

def drive_create(name, type="document", starred=False, description=None, path=None, overwrite=False):
    # Simulate the overwrite = FALSE error
    if not overwrite and name == "VisiCalc" and path is not None:
        # Only error if we've already created it (simulated by checking a global list)
        if any(f.name == "VisiCalc" for f in drive_files):
            raise RuntimeError("File already exists")
    
    res = DriveResource(name, type, starred, description)
    drive_files.append(res)
    return res

def drive_mkdir(name):
    return drive_create(name, type="folder")

def drive_browse(item):
    print(f"Browsing {item.name}...")

def drive_ls(path):
    # Simulating listing files in a folder
    return [f.name for f in drive_files if path == "b4xl" and f.name != "b4xl"]

def drive_rm(*args):
    for arg in args:
        if arg in drive_files:
            drive_files.remove(arg)

def pluck(obj, key, index, final_key):
    # Mimic purrr::pluck(wordstar, "drive_resource", 1, "starred")
    # R's 1-indexing becomes 0-indexing in Python
    try:
        return obj[key][index-1][final_key]
    except (KeyError, IndexError, TypeError):
        return getattr(obj, final_key, None) if hasattr(obj, 'drive_resource') else None

drive_files = []

# Main execution block
if drive_has_token():
    # Create a blank Google Doc named 'WordStar'
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred? YES
    # Use a helper to simulate pluck behavior on the mock object
    pluck_val = wordstar.drive_resource[0]["starred"]

    # Create a blank Google Slides presentation
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description? YES
    pluck_val_1 = execuvision.drive_resource[0]["description"]

    # check out the new presentation
    drive_browse(execuvision)

    # Create folder 'b4xl'
    b4xl = drive_mkdir("b4xl")
    drive_create("VisiCalc", path=b4xl, type="spreadsheet")

    # Another way to create a Google Sheet in folder 'b4xl'
    drive_create("b4xl/SuperCalc", type="spreadsheet")

    # Yet another way to create a new file in a folder
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # Did we really create those Sheets in the intended folder? YES
    drive_ls_result = drive_ls("b4xl")

    try:
        # `overwrite = FALSE` errors if file already exists
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except RuntimeError:
        pass

    # `overwrite = TRUE` proceeds
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
    drive_rm(wordstar, b4xl, execuvision)