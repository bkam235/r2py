# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

import pandas as pd
import numpy as np

# --- Mocking googledrive behavior for execution equivalence ---
class Dribble:
    def __init__(self, data):
        self.data = data
    def __getitem__(self, key):
        return self.data[key]
    def __len__(self):
        return len(self.data['id'])
    def __repr__(self):
        return f"dribble({self.data})"

# Mock state to track "Drive" files
DRIVE_STATE = {
    "files": {},
    "token_present": True
}

def drive_has_token():
    return DRIVE_STATE["token_present"]

def drive_mime_type(type_val):
    mapping = {
        "document": "application/vnd.google-apps.document",
        "presentation": "application/vnd.google-apps.presentation",
        "spreadsheet": "application/vnd.google-apps.spreadsheet",
        "folder": "application/vnd.google-apps.folder",
        "application/vnd.google-apps.folder": "application/vnd.google-apps.folder"
    }
    return mapping.get(type_val, type_val)

def drive_create(name, path=None, type=None, overwrite=None, **kwargs):
    # Path handling
    parent_id = None
    if path is not None:
        # If path is a Dribble/object, get ID, otherwise treat as name
        if hasattr(path, 'data'):
            parent_id = path.data['id'][0]
        elif isinstance(path, str):
            # Search for folder by name
            for fid, fmeta in DRIVE_STATE["files"].items():
                if fmeta['name'] == path and fmeta['mimeType'] == "application/vnd.google-apps.folder":
                    parent_id = fid
                    break
    
    # Handle name if path was provided as "folder/file"
    final_name = name
    if isinstance(name, str) and "/" in name:
        parts = name.split("/")
        final_name = parts[-1]
        # This is a simplified path resolution
        for fid, fmeta in DRIVE_STATE["files"].items():
            if fmeta['name'] == parts[0] and fmeta['mimeType'] == "application/vnd.google-apps.folder":
                parent_id = fid
                break

    # Overwrite logic
    existing = [fid for fid, fmeta in DRIVE_STATE["files"].items() 
                if fmeta['name'] == final_name and fmeta.get('parent') == parent_id]
    
    if existing:
        if overwrite is False:
            raise FileExistsError(f"File {final_name} already exists")
        elif overwrite is True:
            for fid in existing:
                del DRIVE_STATE["files"][fid]
    
    # Create file
    file_id = f"id_{final_name}_{len(DRIVE_STATE['files'])}"
    mime = drive_mime_type(type)
    resource = {
        "id": file_id,
        "name": final_name,
        "mimeType": mime,
        "starred": kwargs.get("starred", False),
        "description": kwargs.get("description", ""),
        "webViewLink": f"https://drive.google.com/file/{file_id}"
    }
    DRIVE_STATE["files"][file_id] = {**resource, "parent": parent_id}
    
    return Dribble({
        "name": [final_name],
        "id": [file_id],
        "drive_resource": [resource]
    })

def drive_mkdir(name, path=None, overwrite=None, **kwargs):
    return drive_create(name, path=path, type="folder", overwrite=overwrite, **kwargs)

def drive_ls(path=None, **kwargs):
    parent_id = None
    if path is not None:
        if hasattr(path, 'data'):
            parent_id = path.data['id'][0]
        elif isinstance(path, str):
            for fid, fmeta in DRIVE_STATE["files"].items():
                if fmeta['name'] == path and fmeta['mimeType'] == "application/vnd.google-apps.folder":
                    parent_id = fid
                    break
    
    results = [fmeta for fid, fmeta in DRIVE_STATE["files"].items() if fmeta.get('parent') == parent_id]
    return results

def drive_browse(file):
    # Mimics browsing by returning the link
    if hasattr(file, 'data'):
        print(file.data['drive_resource'][0]['webViewLink'])
    return file

def drive_rm(*args, **kwargs):
    for arg in args:
        if hasattr(arg, 'data'):
            fid = arg.data['id'][0]
            if fid in DRIVE_STATE["files"]:
                del DRIVE_STATE["files"][fid]

def pluck(x, *indices):
    # Simplified purrr::pluck
    curr = x
    for idx in indices:
        if isinstance(curr, dict):
            curr = curr.get(idx)
        elif isinstance(curr, list):
            curr = curr[idx]
    return curr

# --- Start of translated script ---

if drive_has_token():
    # Create a blank Google Doc named 'WordStar' in
    # your 'My Drive' root folder and star it
# r2py:entity:wordstar
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred? YES
# r2py:entity:pluck
    print(pluck(wordstar, "drive_resource", 0, "starred"))

    # Create a blank Google Slides presentation in
    # the root folder, and set its description
# r2py:entity:execuvision
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description? YES
# r2py:entity:pluck_1
    print(pluck(execuvision, "drive_resource", 0, "description"))

    # check out the new presentation
# r2py:entity:drive_browse
    drive_browse(execuvision)

    # Create folder 'b4xl' in the root folder,
    # then create an empty new Google Sheet in it
# r2py:entity:b4xl
    b4xl = drive_mkdir("b4xl")
# r2py:entity:drive_create
    drive_create("VisiCalc", path=b4xl, type="spreadsheet")

    # Another way to create a Google Sheet in the folder 'b4xl'
# r2py:entity:drive_create_1
    drive_create("b4xl/SuperCalc", type="spreadsheet")

    # Yet another way to create a new file in a folder,
    # this time specifying parent `path` as a character
# r2py:entity:drive_create_2
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # Did we really create those Sheets in the intended folder? YES
# r2py:entity:drive_ls
    print(drive_ls("b4xl"))

    # `overwrite = FALSE` errors if file already exists at target filepath
    # THIS WILL ERROR!
# r2py:entity:drive_create_3
    try:
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except FileExistsError as e:
        print(f"Caught expected error: {e}")

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
# r2py:entity:drive_create_4
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
# r2py:entity:drive_rm
    drive_rm(wordstar, b4xl, execuvision)