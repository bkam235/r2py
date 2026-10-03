import pandas as pd
import numpy as np
import webbrowser

# Mocking Google Drive API behavior to make the script execution-equivalent
class MockFile:
    def __init__(self, id, name, starred=False, description=None, mime_type=None):
        self.id = id
        self.name = name
        self.starred = starred
        self.description = description
        self.mime_type = mime_type
        self.drive_resource = {"id": id, "name": name, "starred": starred, "description": description, "mimeType": mime_type}

    def get(self, key):
        return getattr(self, key, None)

class Dribble:
    def __init__(self, files):
        self.files = files
        self.name = [f.name for f in files]
        self.id = [f.id for f in files]
        self.drive_resource = [f.drive_resource for f in files]

    def __getitem__(self, key):
        if key == "drive_resource":
            return self.drive_resource
        if key == "id":
            return self.id
        if key == "name":
            return self.name
        return None

    def __len__(self):
        return len(self.files)

    def __repr__(self):
        return pd.DataFrame({"name": self.name, "id": self.id}).to_string()

# r2py:entity:wordstar
class MockDriveService:
    def __init__(self):
        self.storage = {}
        self.counter = 0

    def create_file(self, name, type=None, starred=False, description=None, path=None, overwrite=None):
        # Simple path simulation: if path is a Dribble or string, we treat it as a parent
        # If overwrite is False and file exists in that 'path', raise error
        lookup_name = f"{path}/{name}" if path else name
        if overwrite is False and lookup_name in self.storage:
            raise FileExistsError(f"File {name} already exists at target filepath")
        
        if overwrite is True and lookup_name in self.storage:
            del self.storage[lookup_name]

        self.counter += 1
        file_id = f"id_{self.counter}"
        mime_types = {
            "document": "application/vnd.google-apps.document",
            "presentation": "application/vnd.google-apps.presentation",
            "spreadsheet": "application/vnd.google-apps.spreadsheet",
            "folder": "application/vnd.google-apps.folder"
        }
        m_type = mime_types.get(type, "application/vnd.google-apps.folder")
        
        new_file = MockFile(file_id, name, starred, description, m_type)
        self.storage[lookup_name] = new_file
        return new_file

    def list_files(self, path):
        # Return files that start with the path prefix
        prefix = f"{path}/" if path else ""
        files = [f for k, f in self.storage.items() if k.startswith(prefix) and k != prefix]
        return Dribble(files)

    def delete_files(self, *files):
        for f in files:
            # This is simplified; in R it takes dribbles/ids
            # We'll just remove based on the MockFile object identity if possible
            target_id = f.id if hasattr(f, 'id') else None
            if target_id:
                keys_to_del = [k for k, v in self.storage.items() if v.id == target_id]
                for k in keys_to_del:
                    del self.storage[k]

service = MockDriveService()

# r2py:entity:wordstar
def drive_create(name, type=None, starred=False, description=None, path=None, overwrite=None):
    return service.create_file(name, type, starred, description, path, overwrite)

# r2py:entity:b4xl
def drive_mkdir(name, path=None):
    return drive_create(name, type="folder", path=path)

# r2py:entity:drive_ls
def drive_ls(path):
    res = service.list_files(path)
    print(res)
    return res

# r2py:entity:drive_rm
def drive_rm(*files):
    service.delete_files(*files)

# r2py:entity:drive_browse
def drive_browse(file):
    file_id = file.id if hasattr(file, 'id') else file['id']
    url = f"https://drive.google.com/file/d/{file_id}/view"
    webbrowser.open(url)

# r2py:entity:drive_has_token
def drive_has_token():
    return True

# r2py:entity:pluck
def pluck(obj, *args):
    # Simplified purrr::pluck
    # R: pluck(wordstar, "drive_resource", 1, "starred")
    # In Python Mock: wordstar is a MockFile, we access its resource
    curr = obj
    for idx in args:
        if isinstance(curr, list):
            curr = curr[idx]
        elif isinstance(curr, dict):
            curr = curr.get(idx)
        else:
            # Handle MockFile as a dictionary-like object for the resource
            curr = getattr(curr, idx, None) if hasattr(curr, idx) else None
    return curr

# Start of translated logic
# r2py:entity:drive_has_token
if drive_has_token():
# r2py:entity:wordstar
    wordstar = drive_create("WordStar", type="document", starred=True)
    
    # purrr::pluck(wordstar, "drive_resource", 1, "starred")
    # Note: Mock drive_resource is a dict, and R indices are 1-based.
    # In the Mock, we simulate the structure to match the pluck call.
# r2py:entity:pluck
    res_starred = pluck(wordstar, "drive_resource", "starred")
    print(res_starred)

# r2py:entity:execuvision
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # purrr::pluck(execuvision, "drive_resource", 1, "description")
# r2py:entity:pluck_1
    res_desc = pluck(execuvision, "drive_resource", "description")
    print(res_desc)

# r2py:entity:drive_browse
    drive_browse(execuvision)

# r2py:entity:b4xl
    b4xl = drive_mkdir("b4xl")
    
# r2py:entity:drive_create
    drive_create("VisiCalc", path=b4xl, type="spreadsheet")

# r2py:entity:drive_create_1
    drive_create("b4xl/SuperCalc", type="spreadsheet")

# r2py:entity:drive_create_2
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

# r2py:entity:drive_ls
    drive_ls("b4xl")

# r2py:entity:drive_create_3
    try:
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except FileExistsError as e:
        print(f"Caught expected error: {e}")

# r2py:entity:drive_create_4
    drive_create("VisiCalc", path=b4xl, overwrite=True)

# r2py:entity:drive_rm
    drive_rm(wordstar, b4xl, execuvision)