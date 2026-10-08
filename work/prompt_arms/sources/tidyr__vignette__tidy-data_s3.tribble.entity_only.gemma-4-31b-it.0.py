import pandas as pd
import numpy as np

# suppressPackageStartupMessages(library(tidyr))
# import_tidyr

def tribble_equivalent():
    data = {
        "assessment": ["quiz1", "quiz2", "test1"],
        "Billy": [np.nan, "D", "C"],
        "Suzy": ["F", np.nan, np.nan],
        "Lionel": ["B", "C", "B"],
        "Jenny": ["A", "A", "B"]
    }
    df = pd.DataFrame(data)
    
    # Simulate tibble printing format
    print("# A tibble: 3 × 5")
    print("assessment Billy Suzy  Lionel Jenny")
    print("<chr>      <chr> <chr> <chr>  <chr>")
    
    # Format rows to match R output
    for i, row in df.iterrows():
        row_str = []
        for val in row:
            if pd.isna(val):
                row_str.append("<NA>")
            else:
                row_str.append(str(val))
        # R's print adds a leading index
        print(f"{i+1} {'  '.join(row_str).replace('  ', ' ')}")
    
    return df

# Execute tribble and trigger printing
tribble = tribble_equivalent()