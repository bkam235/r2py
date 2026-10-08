# Translated from R script using googledrive package
# Since googledrive has no Python equivalent, we simulate its behavior
# with mock functions that return appropriate data structures.

import sys

# Mock implementation of googledrive functions
class MockDriveResource:
    """Represents a Google Drive resource (file/folder)."""
    def __init__(self, name, file_type, **kwargs):
        self.drive_resource = [{
            'name': name,
            'mimeType': self._get_mime_type(file_type),
            'starred': kwargs.get('starred', False),
            'description': kwargs.get('description', None),
            'id': f'{name.replace(" ", "_").lower()}_{id(self)}'
        }]
        self.id = self.drive_resource[0]['id']
    
    @staticmethod
    def _get_mime_type(file_type):
        types = {
            'document': 'application/vnd.google-apps.document',
            'presentation': 'application/vnd.google-apps.presentation',
            'spreadsheet': 'application/vnd.google-apps.spreadsheet',
            'folder': 'application/vnd.google-apps.folder'
        }
        return types.get(file_type, 'application/octet-stream')

def drive_create(name, type, **kwargs):
    """Mock implementation of drive_create."""
    return MockDriveResource(name, type, **kwargs)

def drive_mkdir(name):
    """Mock implementation of drive_mkdir."""
    return MockDriveResource(name, 'folder')

def drive_browse(resource):
    """Mock implementation of drive_browse."""
    print(f"Opening: {resource.drive_resource[0]['name']}")

def drive_ls(path):
    """Mock implementation of drive_ls."""
    return {'files': []}

def drive_rm(*resources):
    """Mock implementation of drive_rm."""
    for resource in resources:
        pass  # Simulate deletion

def pluck(obj, *keys):
    """Mock implementation of purrr::pluck."""
    current = obj
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list):
            try:
                current = current[int(key) - 1]  # R uses 1-based indexing
            except (IndexError, ValueError):
                return None
        elif hasattr(current, key):
            current = getattr(current, key)
        else:
            return None
    return current

# Execute the main script body (without the if guard)
# Create a blank Google Doc named 'WordStar' in
# your 'My Drive' root folder and star it
wordstar = drive_create("WordStar", type="document", starred=True)

# is 'WordStar' really starred? YES
pluck_result = pluck(wordstar, "drive_resource", 1, "starred")

# Create a blank Google Slides presentation in
# the root folder, and set its description
execuvision = drive_create(
  "ExecuVision",
  type="presentation",
  description="deeply nested bullet lists FTW"
)

# Did we really set the description? YES
pluck_1 = pluck(execuvision, "drive_resource", 1, "description")

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
# Simulating the error behavior:
try_error = None
try:
    drive_create("VisiCalc", path=b4xl, overwrite=False)
except Exception as e:
    try_error = str(e)

# `overwrite = TRUE` moves an existing file to trash, then proceeds
drive_create("VisiCalc", path=b4xl, overwrite=True)

# Clean up
drive_rm(wordstar, b4xl, execuvision)
