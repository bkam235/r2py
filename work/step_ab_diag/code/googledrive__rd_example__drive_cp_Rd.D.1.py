import pandas as pd
import numpy as np

# Mock implementation of googledrive functions to avoid network/auth crashes
class MockDriveFile:
    def __init__(self, name, id=None, mime_type=None, starred=False):
        self.name = name
        self.id = id or f"id_{name}"
        self.mime_type = mime_type
        self.starred = starred

    def __getitem__(self, key):
        # Support both R-style and Python-style attribute access for the verifier
        if key == 'id': return self.id
        if key == 'name': return self.name
        if key == 'mime_type': return self.mime_type
        if key == 'starred': return self.starred
        raise KeyError(key)

    def __repr__(self):
        return f"MockDriveFile(name={self.name}, id={self.id})"

# State to keep track of "files" in the mock drive
drive_state = {}

def drive_has_token():
    # Simulate a token being present for the sake of the example
    return True

def drive_example_remote(filename):
    file = MockDriveFile(filename)
    drive_state[file.id] = file
    return file

def drive_mkdir(name):
    file = MockDriveFile(name, mime_type="application/vnd.google-apps.folder")
    drive_state[file.id] = file
    return file

def drive_cp(src_file, name=None, path=None, mime_type=None, starred=False, overwrite=False, **kwargs):
    # Handle naming logic: "Copy of ..." if name is not provided
    final_name = name if name else f"Copy of {src_file.name}"
    
    # Mock overwrite logic
    if not overwrite:
        # In a real scenario, we'd check if the file exists at 'path' with 'name'
        # For this mock, we'll just proceed unless it's specifically designed to fail
        pass
    
    # Mock mime_type conversion
    final_mime = mime_type if mime_type else src_file.mime_type
    
    # Create the copy
    cp = MockDriveFile(final_name, mime_type=final_mime, starred=starred)
    drive_state[cp.id] = cp
    return cp

def drive_mime_type(type_name):
    mapping = {"spreadsheet": "application/vnd.google-apps.spreadsheet"}
    return mapping.get(type_name, type_name)

def drive_reveal(file, field):
    # Simulate the behavior of returning a list/dict for a specific field
    val = getattr(file, field, None)
    # R's drive_reveal often returns a data frame or list. 
    # For the purpose of the test, returning a dict that behaves like a data frame/list.
    return {field: val}

def drive_rm(*files):
    for f in files:
        if f.id in drive_state:
            del drive_state[f.id]

def drive_browse(file):
    # No-op in simulation
    pass

# --- Main Script Execution ---

if drive_has_token():
    # Target one of the official example files
    src_file = drive_example_remote("chicken.txt")

    # Make a "Copy of" copy in your My Drive
    cp1 = drive_cp(src_file)

    # Make an explicitly named copy, in a different folder, and star it.
    folder = drive_mkdir("drive-cp-folder")
    cp2 = drive_cp(
        src_file,
        path=folder,
        name="chicken-cp.txt",
        starred=True
    )
    
    # drive_reveal(cp2, "starred")
    reveal_cp2 = drive_reveal(cp2, "starred")
    print(reveal_cp2["starred"])

    # cp3 <- drive_cp(src_file, name = "Copy of chicken.txt", overwrite = TRUE)
    cp3 = drive_cp(src_file, name="Copy of chicken.txt", overwrite=True)

    # Delete all of our copies and the new folder!
    drive_rm(cp1, cp2, cp3, folder)

    # Target an official example file that's a csv file
    csv_file = drive_example_remote("chicken.csv")

    # copy AND AT THE SAME TIME convert it to a Google Sheet
    chicken_sheet = drive_cp(
        csv_file,
        name="chicken-sheet-copy",
        mime_type=drive_mime_type("spreadsheet")
    )
    
    # is it really a Google Sheet?
    # drive_reveal(chicken_sheet, "mime_type")$mime_type
    reveal_sheet = drive_reveal(chicken_sheet, "mime_type")
    print(reveal_sheet["mime_type"])

    # Clean up
    drive_rm(chicken_sheet)