import pandas as pd
import numpy as np

# r2py:entity:tribble
tribble = pd.DataFrame({
    "assessment": ["quiz1", "quiz2", "test1"],
    "Billy": [np.nan, "D", "C"],
    "Suzy": ["F", np.nan, np.nan],
    "Lionel": ["B", "C", "B"],
    "Jenny": ["A", "A", "B"]
})

print(tribble.to_string(index=False))