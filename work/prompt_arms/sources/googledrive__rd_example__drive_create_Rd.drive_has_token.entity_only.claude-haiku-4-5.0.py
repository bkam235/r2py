# Translated from drive_create.Rd example by r2py v0.3.0

# Authentication token (mock)
auth_cred = "Token2.0"

MIME_TYPES = {
    "document": "application/vnd.google-apps.document",
    "presentation": "application/vnd.google-apps.presentation",
    "spreadsheet": "application/vnd.google-apps.spreadsheet",
    "folder": "application/vnd.google-apps.folder"
}

def drive_mime_type(type_val):
    return MIME_TYPES.get(type_val, type_val)

def drive_has_token():
    return auth_cred == "Token2.0"

# Mock file ID counter for simulation
_file_counter = 0
_files_db = {}

def _get_next_id():
    global _file_counter
    _file_counter += 1
    return f"id_{_file_counter}"

class MockDriveFile:
    def __init__(self, name, file_type, **kwargs):
        self.id = _get_next_id()
        self.name = name
        self.type = file_type
        self.mimeType = drive_mime_type(file_type)
        self.drive_resource = [{
            'id': self.id,
            'name': name,
            'mimeType': self.mimeType,
        }]
        if 'starred' in kwargs:
            self.drive_resource[0]['starred'] = kwargs['starred']
        if 'description' in kwargs:
            self.drive_resource[0]['description'] = kwargs['description']
        if 'parents' in kwargs:
            self.drive_resource[0]['parents'] = kwargs['parents']
        _files_db[self.id] = self
    
    def get(self, key, default=None):
        return self.drive_resource[0].get(key, default)

def drive_create(name, type=None, path=None, starred=False, description=None, overwrite=False):
    """Mock implementation of googledrive::drive_create"""
    parents = None
    if path is not None:
        if isinstance(path, MockDriveFile):
            parents = [path.id]
        elif isinstance(path, str):
            # Find folder by name
            for file_id, file_obj in _files_db.items():
                if file_obj.name == path and file_obj.type == "folder":
                    parents = [file_id]
                    break
    
    # Check if file exists (overwrite logic)
    existing = None
    if parents:
        for file_id, file_obj in _files_db.items():
            if file_obj.name == name and 'parents' in file_obj.drive_resource[0]:
                if file_obj.drive_resource[0]['parents'] == parents:
                    existing = file_obj
                    break
    
    if existing and not overwrite:
        raise Exception(f"File '{name}' already exists at path and overwrite=False")
    
    if existing and overwrite:
        del _files_db[existing.id]
    
    kwargs = {}
    if starred:
        kwargs['starred'] = True
    if description:
        kwargs['description'] = description
    if parents:
        kwargs['parents'] = parents
    
    return MockDriveFile(name, type, **kwargs)

def drive_mkdir(name, path=None):
    """Mock implementation of googledrive::drive_mkdir"""
    return drive_create(name, type="folder", path=path)

def drive_browse(file_obj):
    """Mock implementation of googledrive::drive_browse"""
    pass

def drive_ls(path=None):
    """Mock implementation of googledrive::drive_ls"""
    if isinstance(path, MockDriveFile):
        parent_id = path.id
    elif isinstance(path, str):
        parent_id = None
        for file_id, file_obj in _files_db.items():
            if file_obj.name == path:
                parent_id = file_id
                break
    
    result = []
    for file_id, file_obj in _files_db.items():
        if 'parents' in file_obj.drive_resource[0]:
            if parent_id in file_obj.drive_resource[0]['parents']:
                result.append(file_obj)
    return result

def drive_rm(*items):
    """Mock implementation of googledrive::drive_rm"""
    for item in items:
        if isinstance(item, MockDriveFile):
            if item.id in _files_db:
                del _files_db[item.id]

# Main script execution (from withAutoprint block)
if drive_has_token():
    # Create a blank Google Doc named 'WordStar' in
    # your 'My Drive' root folder and star it
    wordstar = drive_create("WordStar", type="document", starred=True)
    
    # is 'WordStar' really starred? YES
    # purrr::pluck(wordstar, "drive_resource", 1, "starred")
    pluck = wordstar.drive_resource[0].get("starred")
    
    # Create a blank Google Slides presentation in
    # the root folder, and set its description
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )
    
    # Did we really set the description? YES
    # purrr::pluck(execuvision, "drive_resource", 1, "description")
    pluck_1 = execuvision.drive_resource[0].get("description")
    
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
    try:
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except Exception:
        pass
    
    # `overwrite = TRUE` moves an existing file to trash, then proceeds
    drive_create("VisiCalc", path=b4xl, overwrite=True)
    
    # Clean up
    drive_rm(wordstar, b4xl, execuvision)