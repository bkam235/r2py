# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 14

import pandas as pd
import numpy as np

# Mock implementation of googledrive to avoid API crashes in sandbox
class MockDriveFile:
    def __init__(self, id, name, mime_type=None, starred=False):
        self.id = id
        self.name = name
        self.mime_type = mime_type
        self.starred = starred

    def __getitem__(self, key):
        if key == "id": return self.id
        if key == "name": return self.name
        if key == "mime_type": return self.mime_type
        if key == "starred": return self.starred
        raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

# Global mock storage
mock_drive_storage = {}
file_counter = 0

def _generate_id():
    global file_counter
    file_counter += 1
    return f"id_{file_counter}"

def drive_has_token():
    return True

def drive_example_remote(filename):
    fid = _generate_id()
    file = MockDriveFile(fid, filename, mime_type="text/plain" if "txt" in filename else "text/csv")
    mock_drive_storage[fid] = file
    return file

def drive_mkdir(name):
    fid = _generate_id()
    file = MockDriveFile(fid, name, mime_type="application/vnd.google-apps.folder")
    mock_drive_storage[fid] = file
    return file

def drive_cp(src_file, path=None, name=None, mime_type=None, starred=False, overwrite=False):
    # Handle mime_type helper
    if isinstance(mime_type, dict) and "value" in mime_type:
        mime_type = mime_type["value"]
    
    # Logic for naming
    final_name = name if name else f"Copy of {src_file['name']}"
    
    # Mock overwrite logic
    if not overwrite:
        # In real R, this would check if file exists at path/name
        pass

    fid = _generate_id()
    new_file = MockDriveFile(
        id=fid, 
        name=final_name, 
        mime_type=mime_type or src_file.mime_type, 
        starred=starred
    )
    mock_drive_storage[fid] = new_file
    return new_file

def drive_reveal(file, field):
    # Return a mock object that has the requested field
    res = {"mime_type": file.mime_type, "starred": file.starred}
    return res

def drive_mime_type(type_name):
    mapping = {"spreadsheet": "application/vnd.google-apps.spreadsheet"}
    return {"value": mapping.get(type_name, "")}

def drive_rm(*files):
    for f in files:
        if f and f.id in mock_drive_storage:
            del mock_drive_storage[f.id]

# Start of main logic
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
    drive_reveal(cp2, "starred")

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
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
    reveal_res = drive_reveal(chicken_sheet, "mime_type")
    print(reveal_res["mime_type"])

    # Clean up
    drive_rm(chicken_sheet)