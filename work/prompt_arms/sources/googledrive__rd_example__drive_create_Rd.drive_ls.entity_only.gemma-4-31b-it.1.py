import pandas as pd
import numpy as np

# Mocking googledrive functionality since actual Google Drive API
# requires authentication not available in the execution environment.
class DriveResource:
    def __init__(self, name, type="file", starred=False, description=None):
        self.name = name
        self.type = type
        self.starred = starred
        self.description = description
        self.id = f"id_{name}"
        self.drive_resource = [{"starred": starred, "description": description}]

class MockDrive:
    def __init__(self):
        self.files = []

    def drive_has_token(self):
        # In the R script, this is the guard. We return True to execute the examples.
        return True

    def drive_create(self, name, type="file", path=None, starred=False, description=None, overwrite=None):
        # Handle path-based naming (e.g., "b4xl/SuperCalc")
        actual_name = name
        if "/" in name:
            actual_name = name.split("/")[-1]
        
        # Simulate overwrite
        existing = [f for f in self.files if f.name == actual_name and (path is None or f.path == path)]
        if existing and overwrite is False:
            raise RuntimeError("File already exists")
        if existing and overwrite is True:
            self.files.remove(existing[0])

        res = DriveResource(actual_name, type=type, starred=starred, description=description)
        res.path = path if path else "root"
        self.files.append(res)
        return res

    def drive_mkdir(self, name, path=None, overwrite=None):
        return self.drive_create(name, type="folder", path=path, overwrite=overwrite)

    def drive_ls(self, path):
        # If path is a DriveResource object, use its id/name
        target_path = path.name if hasattr(path, 'name') else path
        return [f for f in self.files if f.path == target_path]

    def drive_browse(self, resource):
        print(f"Browsing {resource.name}...")

    def drive_rm(self, *resources):
        for res in resources:
            if res in self.files:
                self.files.remove(res)

drive = MockDrive()

def drive_has_token():
    return drive.drive_has_token()

def drive_create(*args, **kwargs):
    return drive.drive_create(*args, **kwargs)

def drive_mkdir(*args, **kwargs):
    return drive.drive_mkdir(*args, **kwargs)

def drive_ls(*args, **kwargs):
    return drive.drive_ls(*args, **kwargs)

def drive_browse(*args, **kwargs):
    return drive.drive_browse(*args, **kwargs)

def drive_rm(*args, **kwargs):
    return drive.drive_rm(*args, **kwargs)

def pluck(obj, key, index, subkey):
    # Simulates purrr::pluck(wordstar, "drive_resource", 1, "starred")
    # R is 1-indexed, Python is 0-indexed
    return obj[key][index-1][subkey]

if drive_has_token():
    # Create a blank Google Doc named 'WordStar' in
    # your 'My Drive' root folder and star it
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred? YES
    pluck(wordstar, "drive_resource", 1, "starred")

    # Create a blank Google Slides presentation in
    # the root folder, and set its description
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description? YES
    pluck(execuvision, "drive_resource", 1, "description")

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
    drive_ls("b4xl")

    try:
        # `overwrite = FALSE` errors if file already exists at target filepath
        # THIS WILL ERROR!
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except RuntimeError:
        pass

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
    drive_rm(wordstar, b4xl, execuvision)