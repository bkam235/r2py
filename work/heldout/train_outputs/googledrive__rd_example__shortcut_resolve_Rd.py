import pandas as pd
import numpy as np
import re

# Mocking the Google Drive environment to ensure execution-equivalence without API keys
class DriveService:
    def __init__(self):
        self.files = {
            "remote_chicken_id": {"id": "remote_chicken_id", "name": "chicken_sheet", "mimeType": "application/vnd.google-apps.spreadsheet"}
        }
        self.counter = 100

    def get_example_remote(self, matches):
        for fid, f in self.files.items():
            if re.search(matches, f["name"], re.IGNORECASE):
                return f
        return None

    def copy(self, file_id, name=None):
        original = self.files.get(file_id)
        if not original:
            raise KeyError(f"File {file_id} not found")
        
        self.counter += 1
        new_id = f"file_{self.counter}"
        new_file = original.copy()
        new_file["id"] = new_id
        if name:
            new_file["name"] = name
        else:
            new_file["name"] = f"Copy of {original['name']}"
        
        self.files[new_id] = new_file
        return new_file

    def create_shortcut(self, target_id, name=None):
        target = self.files.get(target_id)
        if not target:
            raise KeyError(f"Target {target_id} not found")
        
        self.counter += 1
        new_id = f"sc_{self.counter}"
        shortcut = {
            "id": new_id,
            "name": name or f"Shortcut to {target['name']}",
            "mimeType": "application/vnd.google.apps.shortcut",
            "shortcutDetails": {"targetId": target_id}
        }
        self.files[new_id] = shortcut
        return shortcut

    def find(self, pattern=None, file_type=None):
        results = []
        for f in self.files.values():
            if file_type == "shortcut" and f.get("mimeType") != "application/vnd.google.apps.shortcut":
                continue
            if pattern and not re.search(pattern, f["name"]):
                continue
            results.append(f)
        return pd.DataFrame(results)

    def delete(self, file_id):
        if file_id in self.files:
            del self.files[file_id]
            return True
        return False

    def resolve(self, file_id):
        f = self.files.get(file_id)
        if not f:
            return None
        target_id = f.get("shortcutDetails", {}).get("targetId")
        if not target_id:
            return None
        return self.files.get(target_id)

drive_service = DriveService()

# r2py:entity:drive_has_token
def drive_has_token():
    return True

# r2py:entity:drive_example_remote
def drive_example_remote(matches):
    return drive_service.get_example_remote(matches)

# r2py:entity:drive_cp
def drive_cp(file, name=None, path=None):
    # Handle if file is a DataFrame (dribble) or a dict
    fid = file['id'] if isinstance(file, dict) else file.iloc[0]['id']
    return drive_service.copy(fid, name=name)

# r2py:entity:shortcut_create
def shortcut_create(file, name=None, path=None):
    fid = file['id'] if isinstance(file, dict) else file.iloc[0]['id']
    return drive_service.create_shortcut(fid, name=name)

# r2py:entity:sc_dat
def drive_find(pattern=None, type=None):
    return drive_service.find(pattern=pattern, file_type=type)

# r2py:entity:shortcut_resolve
def shortcut_resolve(sc_dat):
    resolved_list = []
    for _, row in sc_dat.iterrows():
        res = drive_service.resolve(row['id'])
        if res:
            resolved_list.append({
                "id": res['id'],
                "name": res['name'],
                "id_shortcut": row['id'],
                "name_shortcut": row['name']
            })
        else:
            resolved_list.append({
                "id": None,
                "name": None,
                "id_shortcut": row['id'],
                "name_shortcut": row['name']
            })
    return pd.DataFrame(resolved_list)

# r2py:entity:drive_rm
def drive_rm(file):
    if isinstance(file, pd.DataFrame):
        for fid in file['id']:
            drive_service.delete(fid)
    elif isinstance(file, dict):
        drive_service.delete(file['id'])

# --- Main Script ---
if drive_has_token():
    # Create a file to make a shortcut to
# r2py:entity:file
    file_remote = drive_example_remote("chicken_sheet")
    file = drive_cp(file_remote, name="chicken-sheet-for-shortcut")

    # Create a shortcut
# r2py:entity:sc1
    sc1 = shortcut_create(file, name="shortcut-1")

    # Create a second shortcut by copying the first
    # Note: drive_cp on a shortcut should maintain its shortcut nature
# r2py:entity:sc1_1
    sc1_1 = drive_cp(sc1, name="shortcut-2")

    # Get the shortcuts
# r2py:entity:sc_dat
    sc_dat = drive_find("-[12]$", type="shortcut")

    # Resolve them
# r2py:entity:resolved
    resolved = shortcut_resolve(sc_dat)

    # Print IDs to match R behavior
    if not resolved.empty:
        print(resolved['id'])
    print(file['id'])

    # Delete the target file
# r2py:entity:drive_rm
    drive_rm(file)

    # (Try to) resolve the shortcuts again
    # Should return None for names/ids as target is gone
    resolved_again = shortcut_resolve(sc_dat)
    print(resolved_again)

    # Clean up
# r2py:entity:drive_rm_1
    drive_rm(sc_dat)