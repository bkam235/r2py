# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

# Mock authentication state
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

# Mock file counter for unique IDs
_file_counter = 0
_files_db = {}  # In-memory database of created files

def _generate_file_id():
    global _file_counter
    _file_counter += 1
    return f"file_{_file_counter}"

def drive_create(name, type=None, starred=False, description=None, path=None):
    """Mock implementation of drive_create"""
    file_id = _generate_file_id()
    mime_type = drive_mime_type(type) if type else None
    
    file_obj = {
        "id": file_id,
        "name": name,
        "mimeType": mime_type,
        "starred": starred,
        "description": description,
        "drive_resource": [{
            "id": file_id,
            "name": name,
            "mimeType": mime_type,
            "starred": starred,
            "description": description
        }]
    }
    
    if path:
        if isinstance(path, dict):
            file_obj["parents"] = [path.get("id")]
        elif isinstance(path, str):
            file_obj["parents"] = [path]
    
    _files_db[file_id] = file_obj
    return file_obj

def drive_mkdir(name, path=None):
    """Mock implementation of drive_mkdir"""
    file_id = _generate_file_id()
    
    folder_obj = {
        "id": file_id,
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "drive_resource": [{
            "id": file_id,
            "name": name,
            "mimeType": "application/vnd.google-apps.folder"
        }]
    }
    
    if path:
        if isinstance(path, dict):
            folder_obj["parents"] = [path.get("id")]
        elif isinstance(path, str):
            folder_obj["parents"] = [path]
    
    _files_db[file_id] = folder_obj
    return folder_obj

def drive_browse(file_obj):
    """Mock implementation of drive_browse"""
    # In a real scenario, this would open the file in a browser
    # For testing, we just return the file object
    return file_obj

def drive_ls(path=None):
    """Mock implementation of drive_ls"""
    # List files in a directory
    results = []
    
    if path:
        if isinstance(path, dict):
            parent_id = path.get("id")
        elif isinstance(path, str):
            parent_id = path
        else:
            parent_id = None
        
        for file_id, file_obj in _files_db.items():
            if "parents" in file_obj and parent_id in file_obj.get("parents", []):
                results.append(file_obj)
    
    return results

def drive_rm(*args):
    """Mock implementation of drive_rm"""
    for item in args:
        if isinstance(item, dict):
            file_id = item.get("id")
            if file_id in _files_db:
                del _files_db[file_id]

# Mock purrr::pluck function
def pluck(obj, *keys):
    """Mock implementation of purrr::pluck"""
    current = obj
    for key in keys:
        if isinstance(key, int):
            # Convert to 0-based indexing
            current = current[key - 1]
        else:
            current = current.get(key, None)
            if current is None:
                return None
    return current

# Create a blank Google Doc named 'WordStar' in
# your 'My Drive' root folder and star it
wordstar = drive_create("WordStar", type="document", starred=True)

# is 'WordStar' really starred? YES
pluck_result_1 = pluck(wordstar, "drive_resource", 1, "starred")

# Create a blank Google Slides presentation in
# the root folder, and set its description
execuvision = drive_create(
    "ExecuVision",
    type="presentation",
    description="deeply nested bullet lists FTW"
)

# Did we really set the description? YES
pluck_result_2 = pluck(execuvision, "drive_resource", 1, "description")

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
except Exception as e:
    pass

# `overwrite = TRUE` moves an existing file to trash, then proceeds
drive_create("VisiCalc", path=b4xl, overwrite=True)

# Clean up
drive_rm(wordstar, b4xl, execuvision)
