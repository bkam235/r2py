# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 16

import pandas as pd

# r2py:entity:gs4_has_token
def gs4_has_token() -> bool:
    """Check if a valid Google Sheets token is available."""
    return False

# r2py:entity:gs4_example
def gs4_example(matches: str) -> str:
    """Returns a mock ID for an example sheet."""
    return f"id_of_example_{matches}"

# r2py:entity:range_read
def range_read(ss, sheet=None, range_val=None, col_names=True, col_types=None, na="", trim_ws=True, skip=0, n_max=float('inf'), guess_max=1000, name_repair="unique"):
    """Read a range from a Google Sheet."""
    # Mock data for the 'deaths' example
    if ss == "id_of_example_deaths" and range_val == "other_data":
        data = {
            'col1': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
            'col2': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'col3': [10.1, 20.2, 30.3, 40.4, 50.5, 60.6, 70.7, 80.8, 90.9, 100.1],
            'col4': [True, False, True, False, True, False, True, False, True, False]
        }
        return pd.DataFrame(data)
    
    # For replica check, return the combined data simulated by the operations
    return pd.DataFrame({
        'col1': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
        'col2': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'col3': [10.1, 20.2, 30.3, 40.4, 50.5, 60.6, 70.7, 80.8, 90.9, 100.1],
        'col4': [True, False, True, False, True, False, True, False, True, False]
    })

# r2py:entity:ss
def gs4_create(name="random-sheet", sheets=None):
    """Create a new Google Sheet."""
    print(f"Creating new Sheet: {name}")
    return f"id_of_{name}"

# r2py:entity:sheet_append
def sheet_append(ss, data, sheet=1):
    """Append data to a Google Sheet."""
    print(f"Appending {len(data)} row(s) to sheet {sheet}.")
    return ss

# r2py:entity:gs4_find
def gs4_find(name: str) -> dict:
    """Find a Google Sheet by name."""
    return {"name": name, "id": f"id_of_{name}"}

# r2py:entity:drive_trash
def drive_trash(file: dict) -> None:
    """Move a file to trash."""
    print(f"Moving {file.get('name', 'file')} to trash")

# r2py:entity:gs4_has_token
if gs4_has_token():
    # recreate the table of "other" deaths
# r2py:entity:deaths
    deaths = range_read(gs4_example("deaths"), range_val="other_data", col_types="????DD")

    # split the data into 3 pieces
# r2py:entity:deaths_one
    deaths_one = deaths.iloc[0:5]
# r2py:entity:deaths_two
    deaths_two = deaths.iloc[5:6]
# r2py:entity:deaths_three
    deaths_three = deaths.iloc[6:10]

    # create a Sheet and send the first chunk
# r2py:entity:ss
    ss = gs4_create("sheet-append-demo", sheets={"deaths": deaths_one})

    # append a single row
# r2py:entity:sheet_append
    sheet_append(ss, deaths_two)

    # append remaining rows
# r2py:entity:sheet_append_1
    sheet_append(ss, deaths_three)

    # read and check against the original
# r2py:entity:deaths_replica
    deaths_replica = range_read(ss, col_types="????DD")
# r2py:entity:identical
    print(deaths.equals(deaths_replica))

    # clean up
# r2py:entity:gs4_find
    file_info = gs4_find("sheet-append-demo")
# r2py:entity:drive_trash
    drive_trash(file_info)