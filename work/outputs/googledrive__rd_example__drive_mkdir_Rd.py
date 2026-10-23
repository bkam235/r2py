import pandas as pd
import numpy as np

# Mock Drive State to simulate Google Drive behavior
class MockDrive:
    def __init__(self):
        self.files = {}  # id -> {name, path, starred, description, is_folder}
        self.counter = 0

    def _get_next_id(self):
        self.counter += 1
        return f"id_{self.counter}"

    def find_by_path(self, path):
        if path is None:
            return None
        # Handle cases where path is already a folder object (dict)
        if isinstance(path, dict):
            return path.get('id')
        
        # Simple path lookup
        for fid, file in self.files.items():
            if file['name'] == path.split('/')[-1]:
                return fid
        return None

    def mkdir(self, name, path=None, starred=False, description=None, overwrite=False):
        # Extract name from path if provided as 'parent/child'
        actual_name = name
        parent_path = path
        if '/' in name:
            parts = name.rsplit('/', 1)
            parent_path = parts[0]
            actual_name = parts[1]

        # Determine parent_id
        parent_id = self.find_by_path(parent_path) if parent_path else None

        # Check existence
        existing_id = None
        for fid, file in self.files.items():
            if file['name'] == actual_name:
                # Check if it's in the correct parent folder
                if parent_id and file.get('parent_id') == parent_id:
                    existing_id = fid
                    break
                elif not parent_id and file.get('parent_id') is None:
                    existing_id = fid
                    break

        if existing_id:
            if not overwrite:
                raise FileExistsError(f"Item already exists at target filepath: {actual_name}")
            else:
                # Simulate moving to trash by removing from active files
                del self.files[existing_id]

        # Create new folder
        fid = self._get_next_id()
        self.files[fid] = {
            'id': fid,
            'name': actual_name,
            'parent_id': parent_id,
            'starred': starred,
            'description': description,
            'is_folder': True,
            'drive_resource': {'starred': starred, 'description': description} # Mimic R's nested structure
        }
        # The R object usually returns the resource in a specific structure
        return {'id': fid, 'name': actual_name, 'drive_resource': [{'starred': starred, 'description': description}]}

    def create(self, name, path=None):
        # drive_create is more generic, but for this example, it behaves like mkdir
        return self.mkdir(name, path=path)

    def ls(self, path):
        parent_id = self.find_by_path(path)
        results = []
        for fid, file in self.files.items():
            if file.get('parent_id') == parent_id:
                results.append({'name': file['name'], 'id': fid})
        return pd.DataFrame(results)

    def rm(self, folder_obj):
        fid = folder_obj['id']
        if fid in self.files:
            del self.files[fid]

drive_env = MockDrive()

# r2py:entity:ghi
def drive_mkdir(name, path=None, starred=False, description=None, overwrite=False):
    return drive_env.mkdir(name, path=path, starred=starred, description=description, overwrite=overwrite)

# r2py:entity:drive_create
def drive_create(name, path=None):
    return drive_env.create(name, path=path)

# r2py:entity:drive_ls
def drive_ls(path):
    return drive_env.ls(path)

# r2py:entity:drive_rm
def drive_rm(folder_obj):
    drive_env.rm(folder_obj)

# r2py:entity:drive_has_token
def drive_has_token():
    return True

# r2py:entity:pluck
def pluck(x, *indices):
    curr = x
    try:
        for idx in indices:
            if isinstance(curr, list):
                curr = curr[idx - 1]
            elif isinstance(curr, dict):
                curr = curr[idx]
        return curr
    except (IndexError, KeyError):
        return None

# Main execution logic
# suppressPackageStartupMessages is a no-op in Python
# r2py:entity:drive_has_token
if drive_has_token():
    # r2py:entity:ghi
# r2py:entity:ghi
    ghi = drive_mkdir("ghi")
    
    # r2py:entity:jkl
# r2py:entity:jkl
    # 'ghi/jkl' as a name is handled by our mock as nested
    jkl = drive_mkdir("ghi/jkl", starred=True)

    # r2py:entity:pluck
# r2py:entity:pluck
    print(pluck(jkl, "drive_resource", 1, "starred"))

    # r2py:entity:drive_mkdir (mno)
# r2py:entity:drive_mkdir
    drive_mkdir("mno", path="ghi")

    # r2py:entity:pqr
# r2py:entity:pqr
    pqr = drive_mkdir("pqr", path=ghi, description="I am a folder")

    # r2py:entity:pluck_1
# r2py:entity:pluck_1
    print(pluck(pqr, "drive_resource", 1, "description"))

    try:
        # r2py:entity:drive_create
# r2py:entity:drive_create
        drive_create("name-squatter-mkdir", path=ghi)
        # r2py:entity:drive_mkdir_1
# r2py:entity:drive_mkdir_1
        drive_mkdir("name-squatter-mkdir", path=ghi, overwrite=False)
    except FileExistsError as e:
        print(f"Caught expected error: {e}")

    # r2py:entity:drive_mkdir_2
# r2py:entity:drive_mkdir_2
    drive_mkdir("name-squatter-mkdir", path=ghi, overwrite=True)

    # r2py:entity:drive_ls
# r2py:entity:drive_ls
    print(drive_ls("ghi"))

    # r2py:entity:drive_rm
# r2py:entity:drive_rm
    drive_rm(ghi)