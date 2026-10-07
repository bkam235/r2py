import numpy as np
import pandas as pd
import builtins

def r_factor(x=None, levels=None, labels=None, exclude=np.nan, ordered=False, nmax=None):
    # Handle default x
    if x is None:
        x_vec = np.array([], dtype=object)
    elif isinstance(x, (list, np.ndarray, pd.Series)):
        x_vec = np.array(x, dtype=object)
    else:
        x_vec = np.array([x], dtype=object)

    # Handle names (like R's names(x))
    nx = None
    if isinstance(x, pd.Series):
        nx = x.index

    # matchAsChar logic
    is_char = x_vec.dtype == object or x_vec.dtype == 'U' or x_vec.dtype == 'S'
    is_int = np.issubdtype(x_vec.dtype, np.integer)
    is_log = np.issubdtype(x_vec.dtype, np.bool_)
    match_as_char = not (is_char or is_int or is_log)

    if levels is None:
        if nmax is not None:
            y = pd.unique(x_vec)
            if len(y) > nmax:
                y = y[:nmax]
        else:
            y = pd.unique(x_vec)
        
        y_sorted = np.sort(y[~pd.isna(y)])
        levels_vec = y_sorted
    else:
        levels_vec = np.array(levels, dtype=object)

    if match_as_char:
        x_vec = x_vec.astype(str)

    # levels <- levels[is.na(match(levels, exclude))]
    if exclude is not np.nan:
        mask = np.array([val != exclude for val in levels_vec])
        levels_vec = levels_vec[mask]
    elif np.isnan(exclude) if np.isscalar(exclude) else np.any(pd.isna(exclude)):
        mask = ~pd.isna(levels_vec)
        levels_vec = levels_vec[mask]

    # f <- match(x, levels)
    f_indices = []
    for val in x_vec:
        found = False
        for i, lvl in enumerate(levels_vec):
            if val == lvl:
                f_indices.append(i + 1)
                found = True
                break
        if not found:
            f_indices.append(np.nan)
    
    f_indices = np.array(f_indices)

    # labels logic
    if labels is None:
        final_labels = levels_vec.astype(str)
    else:
        # Ensure labels is a list/array for length checking
        if isinstance(labels, (str, int, float, bool)) or (not hasattr(labels, '__len__')):
            labels_vec = np.array([labels], dtype=object)
        else:
            labels_vec = np.array(labels, dtype=object)
            
        nlab = len(labels_vec)
        nlevs_count = len(levels_vec)
        
        if nlab == nlevs_count:
            # R's logic: nlevs <- unique(xlevs <- as.character(labels))
            # f <- match(xlevs, nlevs)[f]
            # This maps original indices to indices of unique labels
            xlevs = labels_vec.astype(str)
            nlevs = pd.unique(xlevs)
            
            # We map the indices in f to the actual label strings
            final_labels = labels_vec
        elif nlab == 1:
            label_prefix = str(labels_vec[0])
            final_labels = np.array([f"{label_prefix}{i+1}" for i in range(nlevs_count)])
        else:
            raise ValueError(f"invalid 'labels'; length {nlab} should be 1 or {nlevs_count}")

    # Convert indices back to labels
    res = []
    for idx in f_indices:
        if np.isnan(idx):
            res.append(np.nan)
        else:
            # R's factor indexing is 1-based.
            # If final_labels is the same size as levels_vec, we use the index.
            if len(final_labels) == len(levels_vec):
                res.append(str(final_labels[int(idx)-1]))
            else:
                # This handles the case where labels are unique and we remap
                # but for the purpose of this function, the mapping usually aligns.
                res.append(str(final_labels[int(idx)-1]))

    # Result shape handling
    if len(res) == 1 and not isinstance(x, (list, np.ndarray, pd.Series)):
        return res[0]
    
    return np.array(res, dtype=object).tolist()
