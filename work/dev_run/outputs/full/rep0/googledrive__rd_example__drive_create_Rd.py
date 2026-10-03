# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

import pydrive2
import webbrowser

try:
# r2py:entity:drive_has_token
    gdrive = pydrive2.GoogleDrive()
    gdrive.auth
    
    # Create a blank Google Doc named 'WordStar' in
    # your 'My Drive' root folder and star it
    # MIME type for Google Doc is 'application/vnd.google-apps.document'
# r2py:entity:wordstar
    wordstar_file = gdrive.CreateFile({'title': 'WordStar', 'mimeType': 'application/vnd.google-apps.document', 'starred': True})
    wordstar = wordstar_file.upload()

    # is 'WordStar' really starred? YES
    # Equivalent of purrr::pluck(wordstar, "drive_resource", 1, "starred")
# r2py:entity:pluck
    print(wordstar.get('starred'))

    # Create a blank Google Slides presentation in
    # the root folder, and set its description
    # MIME type for Google Slides is 'application/vnd.google-apps.presentation'
# r2py:entity:execuvision
    execuvision_file = gdrive.CreateFile({
        'title': 'ExecuVision', 
        'mimeType': 'application/vnd.google-apps.presentation', 
        'description': 'deeply nested bullet lists FTW'
    })
    execuvision = execuvision_file.upload()

    # Did we really set the description? YES
# r2py:entity:pluck_1
    print(execuvision.get('description'))

    # check out the new presentation
    # drive_browse corresponds to opening the webViewLink
# r2py:entity:drive_browse
    webbrowser.open(execuvision.get('alternateLink'))

    # Create folder 'b4xl' in the root folder,
    # then create an empty new Google Sheet in it
    # MIME type for folder is 'application/vnd.google-apps.folder'
# r2py:entity:b4xl
    b4xl_file = gdrive.CreateFile({'title': 'b4xl', 'mimeType': 'application/vnd.google-apps.folder'})
    b4xl = b4xl_file.upload()
    
    # Create 'VisiCalc' spreadsheet in b4xl folder
# r2py:entity:drive_create
    visicalc_file = gdrive.CreateFile({
        'title': 'VisiCalc', 
        'mimeType': 'application/vnd.google-apps.spreadsheet', 
        'parents': [{'id': b4xl.get('id')}]
    })
    visicalc = visicalc_file.upload()

    # Another way to create a Google Sheet in the folder 'b4xl'
    # (Simulating path-based creation "b4xl/SuperCalc")
# r2py:entity:drive_create_1
    supercalc_file = gdrive.CreateFile({
        'title': 'SuperCalc', 
        'mimeType': 'application/vnd.google-apps.spreadsheet', 
        'parents': [{'id': b4xl.get('id')}]
    })
    supercalc = supercalc_file.upload()

    # Yet another way to create a new file in a folder,
    # this time specifying parent `path` as a character
# r2py:entity:drive_create_2
    lotus_file = gdrive.CreateFile({
        'title': 'Lotus 1-2-3', 
        'mimeType': 'application/vnd.google-apps.spreadsheet', 
        'parents': [{'id': b4xl.get('id')}]
    })
    lotus = lotus_file.upload()

    # Did we really create those Sheets in the intended folder? YES
    # drive_ls("b4xl"): List files where parent is b4xl
# r2py:entity:drive_ls
    query = f"'{b4xl.get('id')}' in parents"
    file_list = gdrive.ListFile({'q': query}).GetList()
    for file in file_list:
        print(file['title'])

    # `overwrite = FALSE` errors if file already exists at target filepath
    # PyDrive2 doesn't natively block duplicates in the API call, 
    # so we check manually to simulate the R behavior.
# r2py:entity:drive_create_3
    existing = gdrive.ListFile({'q': f"name = 'VisiCalc' and '{b4xl.get('id')}' in parents"}).GetList()
    if len(existing) > 0:
        raise FileExistsError("drive_create: file already exists at target filepath")

    # `overwrite = TRUE` moves an existing file to trash, then proceeds
# r2py:entity:drive_create_4
    existing = gdrive.ListFile({'q': f"name = 'VisiCalc' and '{b4xl.get('id')}' in parents"}).GetList()
    if existing:
        for f in existing:
            f.Trash()
    
    visicalc_overwrite_file = gdrive.CreateFile({
        'title': 'VisiCalc', 
        'mimeType': 'application/vnd.google-apps.spreadsheet', 
        'parents': [{'id': b4xl.get('id')}]
    })
    visicalc_final = visicalc_overwrite_file.upload()

    # Clean up
# r2py:entity:drive_rm
    for item in [wordstar, b4xl, execuvision]:
        item.Delete()

except Exception as e:
    print(f"Error during Google Drive operations: {e}")