import pandas as pd
import numpy as np

# Mocking the Google Drive API interaction since actual google-api-python-client
# requires complex authentication not provided in the environment.
# We will simulate the API behavior to ensure structural equivalence.

class MockDriveAPI:
    def __init__(self):
        self.files = {}
        self.counter = 0

    def create_file(self, name, mime_type, parents=None, description=None, starred=False):
        self.counter += 1
        file_id = f"id_{self.counter}"
        
        # Check for overwrite logic if parents are specified
        if parents:
            for fid, fmeta in self.files.items():
                if fmeta['name'] == name and parents[0] == fmeta.get('parent_id'):
                    return "EXISTS"

        file_meta = {
            'id': file_id,
            'name': name,
            'mimeType': mime_type,
            'description': description,
            'starred': starred,
            'parent_id': parents[0] if parents else None,
            'drive_resource': {'id': file_id, 'name': name, 'starred': starred, 'description': description}
        }
        self.files[file_id] = file_meta
        return file_meta

    def list_files(self, q=None):
        # Basic query simulation
        results = []
        for fid, fmeta in self.files.items():
            if q:
                if "name =" in q and fmeta['name'] not in q:
                    continue
                if "parents" in q and fmeta['parent_id'] not in q:
                    continue
            results.append(fmeta)
        return results

    def delete_file(self, file_id):
        if file_id in self.files:
            del self.files[file_id]
            return True
        return False

drive_api = MockDriveAPI()

# r2py:entity:drive_has_token
def drive_has_token():
    return True

# r2py:entity:wordstar
def drive_create(name, path=None, type='document', overwrite=None, **kwargs):
    mime_types = {
        'document': 'application/vnd.google-apps.document',
        'presentation': 'application/vnd.google-apps.presentation',
        'spreadsheet': 'application/vnd.google-apps.spreadsheet',
        'folder': 'application/vnd.google-apps.folder'
    }
    mime_type = mime_types.get(type, type)
    
    # Handle R's rationalize_path_name: if path is "folder/file", split it
    actual_path = path
    actual_name = name
    if path and '/' in path:
        parts = path.rsplit('/', 1)
        actual_path = parts[0]
        actual_name = parts[1] if not name else name # if name is provided, it overrides path's end
    
    # Resolve path to ID
    parent_id = None
    if actual_path:
        # Simplification: search for folder by name
        folders = drive_api.list_files(q=f"name = {actual_path}")
        if folders:
            parent_id = folders[0]['id']
        else:
            # If path is just a name, it might be the root or a non-existent folder
            parent_id = None

    parents = [parent_id] if parent_id else None
    
    # Overwrite check
    existing = [f for f in drive_api.list_files() if f['name'] == actual_name and f['parent_id'] == parent_id]
    if existing:
        if overwrite is False:
            raise FileExistsError(f"File {actual_name} already exists")
        if overwrite is True:
            # Move to trash (simulated by delete)
            drive_api.delete_file(existing[0]['id'])

    starred = kwargs.get('starred', False)
    description = kwargs.get('description', None)
    
    res = drive_api.create_file(actual_name, mime_type, parents=parents, description=description, starred=starred)
    if res == "EXISTS":
        raise FileExistsError(f"File {actual_name} already exists")
    
    # Wrap in a structure resembling a 'dribble' (dataframe-like)
    return {'drive_resource': [res], 'id': res['id'], 'name': res['name']}

# r2py:entity:b4xl
def drive_mkdir(name, path=None, **kwargs):
    return drive_create(name=name, path=path, type='folder', **kwargs)

# r2py:entity:drive_ls
def drive_ls(path=None, **kwargs):
    # Find folder
    folders = drive_api.list_files(q=f"name = {path}")
    if not folders:
        return None
    folder_id = folders[0]['id']
    # List children
    children = [f for f in drive_api.list_files() if f['parent_id'] == folder_id]
    print(pd.DataFrame(children))
    return children

# r2py:entity:drive_browse
def drive_browse(file):
    # file is a dribble-like dict
    res = file['drive_resource'][0]
    print(f"Browsing {res['name']}...")
    return res['id']

# r2py:entity:drive_rm
def drive_rm(*files):
    for f in files:
        if isinstance(f, dict) and 'id' in f:
            drive_api.delete_file(f['id'])
        elif isinstance(f, str): # handle cases where only ID or name is passed
            # simulation: try to find by name if it's a string
            for fid, fmeta in drive_api.files.items():
                if fmeta['name'] == f:
                    drive_api.delete_file(fid)

# r2py:entity:pluck
def pluck(obj, *keys):
    for key in keys:
        try:
            obj = obj[key]
            if isinstance(obj, list) and len(keys) > 0: # Handle R's 1-indexing for lists
                # This is a simplification of purrr::pluck
                pass 
        except (KeyError, IndexError, TypeError):
            return None
    return obj

# Main Script
if drive_has_token():
    # Create 'WordStar'
# r2py:entity:wordstar
    wordstar = drive_create("WordStar", type="document", starred=True)
    
    # purrr::pluck(wordstar, "drive_resource", 1, "starred")
    # Python indexing: drive_resource[0]['starred']
# r2py:entity:pluck
    print(wordstar['drive_resource'][0]['starred'])

    # Create 'ExecuVision'
# r2py:entity:execuvision
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # purrr::pluck(execuvision, "drive_resource", 1, "description")
# r2py:entity:pluck_1
    print(execuvision['drive_resource'][0]['description'])

# r2py:entity:drive_browse
    drive_browse(execuvision)

    # Create folder 'b4xl'
# r2py:entity:b4xl
    b4xl = drive_mkdir("b4xl")
    # Note: drive_mkdir returns a dribble-like object in R; we use the object itself
# r2py:entity:drive_create
    drive_create("VisiCalc", path=b4xl['name'], type="spreadsheet")

    # Another way: path-based name
# r2py:entity:drive_create_1
    drive_create("b4xl/SuperCalc", type="spreadsheet")

    # Character path
# r2py:entity:drive_create_2
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # List files in 'b4xl'
# r2py:entity:drive_ls
    drive_ls("b4xl")

    # overwrite = FALSE errors
    try:
# r2py:entity:drive_create_3
        drive_create("VisiCalc", path=b4xl['name'], overwrite=False)
    except FileExistsError as e:
        print(f"Caught expected error: {e}")

    # overwrite = TRUE proceeds
# r2py:entity:drive_create_4
    drive_create("VisiCalc", path=b4xl['name'], overwrite=True)

    # Clean up
# r2py:entity:drive_rm
    drive_rm(wordstar, b4xl, execuvision)