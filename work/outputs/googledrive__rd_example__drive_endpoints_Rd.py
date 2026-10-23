# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd

def _get_package_metadata():
    """
    Simulates the retrieval of the static endpoint metadata embedded in the googledrive package.
    In a real translation, this would be imported from the package's internal data.
    """
    return [
        {
            "id": "drive.operations.get",
            "httpMethod": "GET",
            "path": "drive/v3/operations/{name}",
            "parameters": {
                "name": {"description": "The name of the operation."}
            },
            "scopes": "drive, drive.file, drive.meet.readonly, drive.readonly",
            "description": "Gets the latest state of a long-running operation. Clients can use this method to poll the operation result at ",
            "response": "Operation"
        },
        {
            "id": "drive.files.list",
            "httpMethod": "GET",
            "path": "drive/v3/files",
            "parameters": {
                "q": {"description": "Search query"}
            },
            "scopes": "drive.readonly",
            "description": "List files in the Drive.",
            "response": "FileList"
        },
        {
            "id": "drive.files.create",
            "httpMethod": "POST",
            "path": "drive/v3/files",
            "parameters": {},
            "scopes": "drive.file",
            "description": "Create a new file.",
            "response": "File"
        },
        {
            "id": "drive.apps.list",
            "httpMethod": "GET",
            "path": "drive/v3/apps",
            "parameters": {
                "appFilterExtensions": {"description": "A comma-separated list of file extensions to limit returned results. All results within the given app query scope which can open any of the given file extensions are included in the response. If `appFilterMimeTypes` are provided as well, the result is a union of the two resulting app lists."}
            },
            "scopes": "drive.readonly",
            "description": "List apps.",
            "response": "AppList"
        },
        {
            "id": "drive.files.delete",
            "httpMethod": "DELETE",
            "path": "drive/v3/files/{fileId}",
            "parameters": {
                "fileId": {"description": "The ID of the file.", "location": "path", "required": True, "type": "string"},
                "supportsAllDrives": {"description": "Whether the requesting application supports both My Drives and shared drives.", "default": "false"}
            },
            "scopes": "drive.file",
            "description": "Delete a file.",
            "response": "Empty"
        }
    ]

# r2py:entity:drive_endpoint
def drive_endpoints():
    """Returns the list of available drive endpoints as a dictionary keyed by ID."""
    data = _get_package_metadata()
    return {item["id"]: item for item in data}

def drive_endpoint(i):
    """Returns a specific drive endpoint by index (1-based) or name."""
    data = _get_package_metadata()
    if isinstance(i, int):
        # R is 1-indexed
        return data[i - 1] if 0 < i <= len(data) else None
    if isinstance(i, str):
        for item in data:
            if item["id"] == i:
                return item
    return None

# r2py:entity:str
def str_mock(object, max_level=2):
    """Python equivalent to R's str() for basic inspection."""
    if isinstance(object, dict):
        print(f"      List of {len(object)}")
        for key, val in object.items():
            if isinstance(val, dict):
                print(f" $ {key}:List of {len(val)}")
                if max_level > 1:
                    for k2, v2 in val.items():
                        type_name = "chr" if isinstance(v2, str) else "List" if isinstance(v2, dict) else "logi" if isinstance(v2, bool) else "num"
                        # R's str output formatting
                        val_str = f"\"{v2}\"" if isinstance(v2, str) else str(v2)
                        print(f"  ..$ {k2:<12} : {type_name} {val_str}")
            else:
                type_name = "chr" if isinstance(val, str) else "num"
                val_str = f"\"{val}\"" if isinstance(val, str) else str(val)
                print(f" $ {key:<12} : {type_name} {val_str}")
    else:
        print(object)

# r2py:entity:str
def head(df, n=3):
    """Simplified head for dictionary-like structures."""
    return {k: df[k] for k in list(df.keys())[:n]}

def print_r_list(d, indent="      "):
    """Helper to print dictionaries in R's recursive list style."""
    if not isinstance(d, dict):
        # R's printing of simple values in a list
        val = str(d).upper() if isinstance(d, bool) else f"\"{d}\""
        print(f"{indent}[1] {val}")
        return

    for k, v in d.items():
        print(f"{indent}${k}")
        if isinstance(v, dict):
            # Recurse with the key as part of the indentation for nested lists
            print_r_list(v, indent + f"${k}")
        else:
            # R's print logic: paths are often printed without quotes, bools are uppercase
            if k == "path":
                print(f"{indent}[1] {v}")
            else:
                val = str(v).upper() if isinstance(v, bool) else f"\"{v}\""
                print(f"{indent}[1] {val}")

# --- Translated Script ---

# suppressPackageStartupMessages(library(googledrive))
# Handled by mock logic.

# str(head(drive_endpoints(), 3), max.level = 2)
# r2py:entity:str
endpoints = drive_endpoints()
endpoints_head = head(endpoints, 3)
str_mock(endpoints_head, max_level=2)

# drive_endpoint("drive.files.delete")
# r2py:entity:drive_endpoint
res1 = drive_endpoint("drive.files.delete")
if res1:
    print_r_list(res1)

# drive_endpoint(4)
# r2py:entity:drive_endpoint_1
res2 = drive_endpoint(4)
if res2:
    print_r_list(res2)