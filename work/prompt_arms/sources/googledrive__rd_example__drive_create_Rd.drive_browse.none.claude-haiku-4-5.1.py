# Translated from R googledrive example
# googledrive is R-only; this creates mock implementations

class MockDriveResource:
    """Mock googledrive drive resource object"""
    def __init__(self, name, file_type=None, description=None, starred=False, parent_id=None):
        self.drive_resource = [{
            'name': name,
            'starred': starred,
            'description': description,
            'id': f'mock_{name.replace(" ", "_")}'
        }]
        self.id = self.drive_resource[0]['id']

def drive_create(name, type=None, description=None, starred=False, path=None, overwrite=False):
    """Mock googledrive drive_create function"""
    return MockDriveResource(name, type, description, starred, path)

def drive_mkdir(path):
    """Mock googledrive drive_mkdir function"""
    return MockDriveResource(path, 'folder')

def drive_browse(file):
    """Mock googledrive drive_browse function"""
    pass

def drive_ls(path):
    """Mock googledrive drive_ls function"""
    return []

def drive_rm(*args):
    """Mock googledrive drive_rm function"""
    pass

def pluck(obj, *keys):
    """Mock purrr pluck function - extract nested element"""
    current = obj
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, (list, tuple)):
            # Convert to 0-indexed for Python (R uses 1-indexed)
            if isinstance(key, int):
                current = current[key - 1]
            else:
                current = current[key]
        else:
            return None
    return current

# Execute the example code
# Create a blank Google Doc named 'WordStar' in your 'My Drive' root folder and star it
wordstar = drive_create("WordStar", type="document", starred=True)

# is 'WordStar' really starred? YES
pluck_result_1 = pluck(wordstar, "drive_resource", 1, "starred")

# Create a blank Google Slides presentation in the root folder, and set its description
execuvision = drive_create(
    "ExecuVision",
    type="presentation",
    description="deeply nested bullet lists FTW"
)

# Did we really set the description? YES
pluck_result_2 = pluck(execuvision, "drive_resource", 1, "description")

# check out the new presentation
drive_browse(execuvision)

# Create folder 'b4xl' in the root folder, then create an empty new Google Sheet in it
b4xl = drive_mkdir("b4xl")
drive_create("VisiCalc", path=b4xl, type="spreadsheet")

# Another way to create a Google Sheet in the folder 'b4xl'
drive_create("b4xl/SuperCalc", type="spreadsheet")

# Yet another way to create a new file in a folder, this time specifying parent `path` as a character
drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

# Did we really create those Sheets in the intended folder? YES
drive_ls("b4xl")

# `overwrite = FALSE` errors if file already exists at target filepath
# THIS WILL ERROR!
try:
    drive_create("VisiCalc", path=b4xl, overwrite=False)
except:
    pass

# `overwrite = TRUE` moves an existing file to trash, then proceeds
drive_create("VisiCalc", path=b4xl, overwrite=True)

# Clean up
drive_rm(wordstar, b4xl, execuvision)