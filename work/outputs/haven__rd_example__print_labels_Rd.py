# Translated from <R script> by r2py v0.3.0
# Model: claude-haiku-4-5  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/haven__rd_example__print_labels_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'haven__rd_example__print_labels_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['var']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np

class HavenLabelled:
    """A class to represent labelled vectors from haven package."""
    
    def __init__(self, data, labels=None, label=None):
        self.data = np.array(data)
        self.labels = labels if labels is not None else {}
        self.label = label
        self._validate()
    
    def _validate(self):
        """Validate the labelled object."""
        if self.labels:
            if not all(isinstance(k, str) for k in self.labels.keys()):
                raise ValueError("labels must have names (keys).")
            label_values = list(self.labels.values())
            if len(label_values) != len(set(label_values)):
                raise ValueError("labels must be unique.")
        
        if self.label is not None:
            if not isinstance(self.label, str):
                raise ValueError("label must be a character vector of length one.")
    
    def __repr__(self):
        return f"HavenLabelled({self.data}, labels={self.labels})"
    
    def __getitem__(self, idx):
        return self.data[idx]
    
    def __len__(self):
        return len(self.data)


# r2py:entity:s2
def labelled(x=None, labels=None, label=None):
    """Create a labelled vector."""
    if x is None:
        x = []
    return HavenLabelled(x, labels=labels, label=label)


def is_labelled(x):
    """Check if object is labelled."""
    return isinstance(x, HavenLabelled)


def format_tagged_na(x, digits=None):
    """Format tagged NA values."""
    if digits is None:
        digits = 6
    formatted = [f"{val:.{digits}g}" if not np.isnan(val) else "NA" for val in x]
    return formatted


# r2py:entity:print_labels
def print_labels(x, name=None):
    """Print labels of a labelled vector."""
    if not is_labelled(x):
        raise ValueError("x must be a labelled vector.")
    
    labels = x.labels
    if not labels:
        return
    
    name_str = name if name is not None else ""
    # Format: Labels:name (no space after colon)
    print(f"Labels:{name_str}")
    
    label_values = list(labels.values())
    label_names = list(labels.keys())
    
    # Create DataFrame with value and label columns
    df = pd.DataFrame({
        'value': label_values,
        'label': label_names
    })
    
    # Print with proper formatting (right-aligned values, left-aligned labels)
    print(df.to_string(index=False))


# Main example code
# r2py:entity:s1
s1 = labelled(["M", "M", "F"], labels={"Male": "M", "Female": "F"})
# r2py:entity:s2
s2 = labelled([1, 1, 2], labels={"Male": 1, "Female": 2})

# r2py:entity:labelled_df
labelled_df = pd.DataFrame({
    's1': s1.data,
    's2': s2.data
})

# Store labelled metadata
labelled_df_labelled = {
    's1': s1,
    's2': s2
}

# r2py:entity:print_labels
for var in labelled_df.columns:
    print_labels(labelled_df_labelled[var], var)