# Translated from googledrive drive_create.Rd examples by r2py v0.3.0
# Mock implementation of googledrive functions for testing

class DriveFile:
    """Simulates a googledrive file object"""
    def __init__(self, name, file_type, **kwargs):
        self.drive_resource = [{
            'id': f'id_{name.replace(" ", "_").lower()}',
            'name': name,
            'mimeType': file_type,
            **kwargs
        }]
    
    def __getitem__(self, key):
        if key == 'drive_resource':
            return self.drive_resource
        return self.drive_resource[0].get(key)

def drive_has_token():
    """Simulate checking if Google Drive token exists"""
    return True

def drive_create(name, type=None, description=None, path=None, starred=False, overwrite=None):
    """Simulate drive_create function"""
    mime_types = {
        'document': 'application/vnd.google-apps.document',
        'presentation': 'application/vnd.google-apps.presentation',
        'spreadsheet': 'application/vnd.google-apps.spreadsheet'
    }
    mime_type = mime_types.get(type, 'application/octet-stream')
    kwargs = {'starred': starred} if starred else {}
    if description:
        kwargs['description'] = description
    return DriveFile(name, mime_type, **kwargs)

def drive_mkdir(name):
    """Simulate drive_mkdir function"""
    return DriveFile(name, 'application/vnd.google-apps.folder')

def drive_browse(file):
    """Simulate drive_browse function"""
    pass

def drive_ls(path):
    """Simulate drive_ls function"""
    return []

def drive_rm(*files):
    """Simulate drive_rm function"""
    pass

def pluck(obj, *keys):
    """Simulate purrr::pluck function"""
    result = obj
    for key in keys:
        if isinstance(key, int):
            result = result[key]
        else:
            result = result[key]
    return result

# Main execution
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
    
    # `overwrite = FALSE` errors if file already exists at target filepath
    # THIS WILL ERROR!
    drive_create("VisiCalc", path=b4xl, overwrite=False)
    
    # `overwrite = TRUE` moves an existing file to trash, then proceeds
    drive_create("VisiCalc", path=b4xl, overwrite=True)
    
    # Clean up
    drive_rm(wordstar, b4xl, execuvision)
