# Translated from R googledrive example
# Package: googledrive (R) -> mocked in Python
# Note: googledrive Python package is not available.
# This translation provides mock/stub implementations to match R structure.

# Mock googledrive functions
class MockDriveResource:
    """Mock object representing a Google Drive resource."""
    def __init__(self, **kwargs):
        self.drive_resource = [kwargs]
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __getitem__(self, key):
        return self.drive_resource[0].get(key)

def drive_has_token():
    """Mock: Check if googledrive has a token."""
    return False  # Return False to skip the example block

def drive_create(name, type=None, starred=False, description=None, path=None):
    """Mock: Create a Google Drive file."""
    resource = {
        'name': name,
        'mimeType': f'application/vnd.google-apps.{type}' if type else 'application/octet-stream',
    }
    if starred:
        resource['starred'] = starred
    if description:
        resource['description'] = description
    return MockDriveResource(**resource)

def drive_mkdir(name):
    """Mock: Create a Google Drive folder."""
    return MockDriveResource(name=name, mimeType='application/vnd.google-apps.folder')

def drive_browse(file):
    """Mock: Open a file in Google Drive."""
    pass

def drive_ls(path):
    """Mock: List files in a Google Drive folder."""
    return []

def drive_rm(*files):
    """Mock: Remove files from Google Drive."""
    pass

def pluck(obj, *keys):
    """Mock: Extract nested values (like purrr::pluck in R)."""
    result = obj
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
        elif isinstance(result, (list, tuple)):
            result = result[key]
        elif hasattr(result, key):
            result = getattr(result, key)
        else:
            return None
    return result

# Main script execution
# The original R code is wrapped in: if (drive_has_token()) withAutoprint({ ... })
# Since drive_has_token() returns False (no credentials), the block is skipped in Python.
# However, per instructions, we remove the guard and execute unconditionally.

# r2py:data_shim managed by the harness ...

# Create a blank Google Doc named 'WordStar' in your 'My Drive' root folder and star it
wordstar = drive_create("WordStar", type="document", starred=True)

# is 'WordStar' really starred? YES
starred_result = pluck(wordstar, "drive_resource", 0, "starred")

# Create a blank Google Slides presentation in the root folder, and set its description
execuvision = drive_create(
    "ExecuVision",
    type="presentation",
    description="deeply nested bullet lists FTW"
)

# Did we really set the description? YES
description_result = pluck(execuvision, "drive_resource", 0, "description")

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
