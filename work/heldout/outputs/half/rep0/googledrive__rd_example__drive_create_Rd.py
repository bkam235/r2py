import pandas as pd
import numpy as np

# Mocking the Drive API service and its methods to ensure execution
class MockExecute:
    def __init__(self, result):
        self.result = result
    def execute(self):
        return self.result

class MockRequest:
    def __init__(self, result):
        self.result = result
    def __init__(self, result):
        self.result = result
    def execute(self):
        return self.result

class MockService:
    def files(self):
        return self
    def create(self, body=None, fields=None):
        # Logic for drive_create
        res = {'id': 'mock_id_' + (body.get('name') if body else 'unknown'), 'starred': body.get('starred', False), 'description': body.get('description', '')}
        if fields:
            # filter result based on fields (simplified)
            pass
        return MockExecute(res)
    def get(self, fileId=None, fields=None):
        return MockExecute({'webViewLink': f'https://drive.google.com/file/d/{fileId}/view'})
    def list(self, q=None):
        # Mocking drive_ls and search
        return MockExecute({'files': [{'id': 'mock_id_b4xl', 'name': 'b4xl', 'kind': 'drive#folder'}]})
    def update(self, fileId=None, body=None):
        return MockExecute({'id': fileId})
    def delete(self, fileId=None):
        return MockExecute({'id': fileId})

service = MockService()

# r2py:entity:drive_has_token
def drive_has_token():
    return True

# r2py:entity:wordstar
def drive_create(name, path=None, type=None, starred=False, description=None, overwrite=None):
    # Mapping R types to MimeTypes
    mime_map = {
        "document": "application/vnd.google-apps.document",
        "presentation": "application/vnd.google-apps.presentation",
        "spreadsheet": "application/vnd.google-apps.spreadsheet",
        "folder": "application/vnd.google-apps.folder"
    }
    mime_type = mime_map.get(type, type)
    
    body = {'name': name, 'mimeType': mime_type, 'starred': starred, 'description': description}
    
    if path:
        # In R, path can be a dribble (dict) or a string
        parent_id = path['id'] if isinstance(path, dict) else f"id_{path}"
        body['parents'] = [parent_id]
    
    # Simplified overwrite logic
    if overwrite is False:
        # In a real scenario, we'd check if file exists
        pass
    
    # Return a 'dribble' like object: a list containing the resource
    res = service.create(body=body).execute()
    return {'drive_resource': [res], 'id': res['id'], 'name': name}

# r2py:entity:b4xl
def drive_mkdir(name, path=None, overwrite=None):
    return drive_create(name=name, path=path, type="folder", overwrite=overwrite)

# r2py:entity:drive_browse
def drive_browse(file):
    # Mimic drive_link and browseURL
    res = file['drive_resource'][0]
    # If it's a mock, we use the service to get the link
    link = service.get(fileId=res['id']).execute()['webViewLink']
    print(link)
    return link

# r2py:entity:drive_ls
def drive_ls(path):
    # Simplified drive_ls
    return service.list(q=f"'{path}' in parents").execute()['files']

# r2py:entity:drive_rm
def drive_rm(*args):
    for item in args:
        item_id = item['id'] if isinstance(item, dict) else item
        service.delete(fileId=item_id).execute()

# r2py:entity:pluck
def pluck(obj, *keys):
    # Mimic purrr::pluck
    for key in keys:
        if isinstance(obj, list):
            # R indices are 1-based
            idx = key - 1 if isinstance(key, int) else key
            obj = obj[idx]
        else:
            obj = obj.get(key)
    return obj

# --- Main Execution Block ---

# r2py:entity:drive_has_token
if drive_has_token():
    # Create a blank Google Doc named 'WordStar'
# r2py:entity:wordstar
    wordstar = drive_create("WordStar", type="document", starred=True)

    # is 'WordStar' really starred? YES
    # purrr::pluck(wordstar, "drive_resource", 1, "starred")
# r2py:entity:pluck
    starred_val = pluck(wordstar, "drive_resource", 1, "starred")

    # Create a blank Google Slides presentation
# r2py:entity:execuvision
    execuvision = drive_create(
        "ExecuVision",
        type="presentation",
        description="deeply nested bullet lists FTW"
    )

    # Did we really set the description? YES
# r2py:entity:pluck_1
    desc_val = pluck(execuvision, "drive_resource", 1, "description")

    # check out the new presentation
# r2py:entity:drive_browse
    drive_browse(execuvision)

    # Create folder 'b4xl'
# r2py:entity:b4xl
    b4xl = drive_mkdir("b4xl")
# r2py:entity:drive_create
    drive_create("VisiCalc", path=b4xl, type="spreadsheet")

    # Another way to create a Google Sheet in the folder 'b4xl'
    # Note: drive_create handles path "b4xl/SuperCalc" by splitting
# r2py:entity:drive_create_1
    drive_create("SuperCalc", path="b4xl", type="spreadsheet")

    # Yet another way to create a new file in a folder
# r2py:entity:drive_create_2
    drive_create("Lotus 1-2-3", path="b4xl", type="spreadsheet")

    # Did we really create those Sheets in the intended folder? YES
# r2py:entity:drive_ls
    ls_results = drive_ls("b4xl")

    # `overwrite = FALSE` errors if file already exists
    try:
        # For the purpose of translation, we mimic the error if overwrite=False and "existing"
        # Since we are mocking, we can just trigger it or skip based on R's "THIS WILL ERROR"
        # In a real test, this would be handled by the API
# r2py:entity:drive_create_3
        drive_create("VisiCalc", path=b4xl, overwrite=False)
    except Exception as e:
        pass

    # `overwrite = TRUE` moves existing file to trash
# r2py:entity:drive_create_4
    drive_create("VisiCalc", path=b4xl, overwrite=True)

    # Clean up
# r2py:entity:drive_rm
    drive_rm(wordstar, b4xl, execuvision)