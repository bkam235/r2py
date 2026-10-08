# Translated from R example by r2py

# googledrive package stub - no Python equivalent available
# Mock the required functions to show the example flow

def drive_has_token():
    """Check if Google Drive authentication token exists."""
    return False  # Simulate no token, preventing example execution

def drive_create(name, path=None, type=None, description=None, starred=False, overwrite=None):
    """Stub for drive_create - creates files/folders on Google Drive."""
    return {"name": name, "type": type, "id": f"id_{name}"}

def drive_mkdir(name, path=None, overwrite=None):
    """Stub for drive_mkdir - creates folder on Google Drive."""
    return drive_create(name, path=path, type="folder", overwrite=overwrite)

def drive_browse(file):
    """Stub for drive_browse - opens file in browser."""
    print(f"Opening {file['name']} in browser")

def drive_ls(path):
    """Stub for drive_ls - lists files in folder."""
    return []

def drive_rm(*files):
    """Stub for drive_rm - removes files from Google Drive."""
    pass

def pluck(obj, *path):
    """Stub for purrr::pluck - extract nested element."""
    result = obj
    for key in path:
        if isinstance(result, dict):
            result = result.get(key)
        elif isinstance(result, (list, tuple)):
            result = result[key] if key < len(result) else None
        else:
            return None
    return result

# withAutoprint context - execute only if drive_has_token() is True
if drive_has_token():
    # Create a blank Google Doc named 'WordStar' in
    # your 'My Drive' root folder and star it
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred? YES
    pluck(wordstar, "drive_resource", 0, "starred")

    # Create a blank Google Slides presentation in
    # the root folder, and set its description
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description? YES
    pluck(execuvision, "drive_resource", 0, "description")

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

    # `overwrite = FALSE` errors if file already exists at target filepath
    # THIS WILL ERROR!
    drive_create("VisiCalc", path=b4xl, overwrite=False)

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
    drive_rm(wordstar, b4xl, execuvision)