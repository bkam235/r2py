import pandas as pd
import numpy as np
import webbrowser

# Mocking the googledrive functionality as it requires API keys and specific auth
# These mocks simulate the behavior described in the R source and the helper functions.

# r2py:entity:drive_has_token
def drive_has_token():
    # Simulate that a token exists for the purpose of the example
    return True

# r2py:entity:wordstar
def drive_mime_type(type_val):
    mime_map = {
        "document": "application/vnd.google-apps.document",
        "presentation": "application/vnd.google-apps.presentation",
        "spreadsheet": "application/vnd.google-apps.spreadsheet",
        "folder": "application/vnd.google-apps.folder",
        "application/vnd.google-apps.folder": "application/vnd.google-apps.folder"
    }
    return mime_map.get(type_val, type_val)

def drive_create(name, path=None, type_val=None, starred=False, description=None, overwrite=None):
    # Logic for overwrite = FALSE (should error if file exists)
    # For the mock, we track "files" in a global list
    global DRIVE_FILES
    
    # Resolve path/name (simplified rationalize_path_name)
    actual_name = name
    actual_path = path
    if path is not None and name is None:
        # Handle cases like drive_create("b4xl/SuperCalc")
        if "/" in path:
            actual_path, actual_name = path.rsplit("/", 1)
        else:
            actual_path = path
            actual_name = "Unnamed"

    # Check for existence
    exists = any(f['name'] == actual_name and f.get('path') == actual_path for f in DRIVE_FILES)
    
    if exists and overwrite is False:
        raise FileExistsError(f"File {actual_name} already exists at target filepath")
    
    if exists and overwrite is True:
        # Move to trash (mocked by removing from list)
        DRIVE_FILES[:] = [f for f in DRIVE_FILES if not (f['name'] == actual_name and f.get('path') == actual_path)]

    mime = drive_mime_type(type_val)
    file_id = f"id_{len(DRIVE_FILES) + 1}"
    
    # Create the "dribble" object structure
    resource = {
        "id": file_id,
        "name": actual_name,
        "mimeType": mime,
        "starred": starred,
        "description": description,
        "webViewLink": f"https://drive.google.com/file/d/{file_id}/view"
    }
    
    # The R object is essentially a data frame (dribble)
    # drive_resource is a list column containing the API response
    dribble = {
        "name": [actual_name],
        "id": [file_id],
        "drive_resource": [resource]
    }
    
    DRIVE_FILES.append({"name": actual_name, "path": actual_path, "id": file_id})
    return dribble

# r2py:entity:b4xl
def drive_mkdir(name, path=None, overwrite=None):
    return drive_create(name, path=path, type_val="folder", overwrite=overwrite)

# r2py:entity:drive_ls
def drive_ls(path):
    # Simplified drive_ls: find files with the given path
    results = [f for f in DRIVE_FILES if f.get('path') == path]
    return results

# r2py:entity:drive_browse
def drive_browse(file):
    # file is a dribble
    link = file["drive_resource"][0]["webViewLink"]
    webbrowser.open(link)
    return link

# r2py:entity:drive_rm
def drive_rm(*args):
    global DRIVE_FILES
    # In reality, this deletes by ID
    # For mock, we just clear the list or specific entries
    DRIVE_FILES[:] = []
    return True

# r2py:entity:pluck
def pluck(obj, *keys):
    # Simplified purrr::pluck
    val = obj
    for key in keys:
        if isinstance(val, list):
            val = val[key]
        elif isinstance(val, dict):
            val = val.get(key)
        else:
            return None
    return val

# Data shim for mock state
DRIVE_FILES = []

# Main execution logic
if drive_has_token():
    # Create a blank Google Doc named 'WordStar' in
    # your 'My Drive' root folder and star it
# r2py:entity:wordstar
    wordstar = drive_create("WordStar", type_val="document", starred=True)

    # is 'WordStar' really starred? YES
# r2py:entity:pluck
    starred_status = pluck(wordstar, "drive_resource", 0, "starred")

    # Create a blank Google Slides presentation in
    # the root folder, and set its description
# r2py:entity:execuvision
    execuvision = drive_create(
        "ExecuVision",
        type_val="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description? YES
# r2py:entity:pluck_1
    description_val = pluck(execuvision, "drive_resource", 0, "description")

    # check out the new presentation
# r2py:entity:drive_browse
    drive_browse(execuvision)

    # Create folder 'b4xl' in the root folder,
    # then create an empty new Google Sheet in it
# r2py:entity:b4xl
    b4xl = drive_mkdir("b4xl")
    # path can be the dribble object (taking its ID/name)
    b4xl_name = b4xl["name"][0]
# r2py:entity:drive_create
    drive_create("VisiCalc", path=b4xl_name, type_val="spreadsheet")

    # Another way to create a Google Sheet in the folder 'b4xl'
# r2py:entity:drive_create_1
    drive_create("b4xl/SuperCalc", type_val="spreadsheet")

    # Yet another way to create a new file in a folder,
    # this time specifying parent `path` as a character
# r2py:entity:drive_create_2
    drive_create("Lotus 1-2-3", path="b4xl", type_val="spreadsheet")

    # Did we really create those Sheets in the intended folder? YES
# r2py:entity:drive_ls
    ls_output = drive_ls("b4xl")

    # `overwrite = FALSE` errors if file already exists at target filepath
    # THIS WILL ERROR!
    try:
# r2py:entity:drive_create_3
        drive_create("VisiCalc", path=b4xl_name, overwrite=False)
    except FileExistsError:
        pass # This is the expected behavior

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
# r2py:entity:drive_create_4
    drive_create("VisiCalc", path=b4xl_name, overwrite=True)

    # Clean up
# r2py:entity:drive_rm
    drive_rm(wordstar, b4xl, execuvision)