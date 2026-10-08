import pandas as pd
import numpy as np

# Mocking googledrive functionality to be execution-equivalent
class MockDriveResource:
    def __init__(self, name, type_val, starred=False, description=None, path=None):
        self.name = name
        self.type = type_val
        self.starred = starred
        self.description = description
        self.path = path
        self.id = f"id_{name}"

    def __getitem__(self, key):
        # Simulating the structure drive_resource[1]["starred"]
        if key == "drive_resource":
            return [self]
        return getattr(self, key, None)

class MockDrive:
    def __init__(self):
        self.files = {}
        self.token = True

    def has_token(self):
        return self.token

    def create(self, name, type_val, starred=False, description=None, path=None, overwrite=False):
        # Logic for path resolution
        folder_path = path
        if isinstance(name, str) and "/" in name:
            folder_path, name = name.split("/", 1)

        # Check if file exists at target path
        existing = [f for f in self.files.values() if f.name == name and f.path == folder_path]
        
        if existing and not overwrite:
            raise RuntimeError("File already exists at target filepath")
        
        if existing and overwrite:
            # Move to trash (simulated by removing from files)
            self.files.pop(existing[0].id)

        res = MockDriveResource(name, type_val, starred, description, path)
        self.files[res.id] = res
        return res

    def mkdir(self, name):
        res = MockDriveResource(name, "folder")
        self.files[res.id] = res
        return res

    def ls(self, path):
        # Return files matching path
        return [f for f in self.files.values() if f.path == path or (isinstance(path, MockDriveResource) and f.path == path.id)]

    def rm(self, *items):
        for item in items:
            if isinstance(item, MockDriveResource):
                self.files.pop(item.id, None)

    def browse(self, item):
        print(f"Browsing {item.name}...")

drive = MockDrive()

# suppressPackageStartupMessages(library(googledrive))
# if (drive_has_token()) withAutoprint({
drive_has_token = drive.has_token()
if drive_has_token:
    # wordstar <- drive_create("WordStar", type = "document", starred = TRUE)
    wordstar = drive.create("WordStar", type_val="document", starred=True)

    # purrr::pluck(wordstar, "drive_resource", 1, "starred")
    pluck = wordstar["drive_resource"][0].starred

    # execuvision <- drive_create("ExecuVision", type = "presentation", description = "deeply nested bullet lists FTW")
    execuvision = drive.create("ExecuVision", type_val="presentation", description="deeply nested bullet lists FTW")

    # purrr::pluck(execuvision, "drive_resource", 1, "description")
    pluck_1 = execuvision["drive_resource"][0].description

    # drive_browse(execuvision)
    drive.browse(execuvision)

    # b4xl <- drive_mkdir("b4xl")
    b4xl = drive.mkdir("b4xl")

    # drive_create("VisiCalc", path = b4xl, type = "spreadsheet")
    drive.create("VisiCalc", path=b4xl, type_val="spreadsheet")

    # drive_create("b4xl/SuperCalc", type = "spreadsheet")
    drive.create("b4xl/SuperCalc", type_val="spreadsheet")

    # drive_create("Lotus 1-2-3", path = "b4xl", type = "spreadsheet")
    drive.create("Lotus 1-2-3", path="b4xl", type_val="spreadsheet")

    # drive_ls("b4xl")
    drive_ls = drive.ls("b4xl")

    # drive_create("VisiCalc", path = b4xl, overwrite = FALSE)
    try:
        drive.create("VisiCalc", path=b4xl, overwrite=False)
    except RuntimeError as e:
        pass # Expected to error

    # drive_create("VisiCalc", path = b4xl, overwrite = TRUE)
    drive.create("VisiCalc", path=b4xl, overwrite=True)

    # drive_rm(wordstar, b4xl, execuvision)
    drive.rm(wordstar, b4xl, execuvision)
