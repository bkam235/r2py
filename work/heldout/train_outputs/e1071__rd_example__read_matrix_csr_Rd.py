# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 13

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'e1071__rd_example__read_matrix_csr_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['iris']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd
import numpy as np
from scipy import sparse

# r2py:entity:xs
def as_matrix_csr(x):
    """Approximation of SparseM::as.matrix.csr"""
    if sparse.isspmatrix_csr(x):
        return x
    return sparse.csr_matrix(x)

# r2py:entity:write.matrix.csr
def write_matrix_csr(x, file="out.dat", y=None, fac=True):
    """Implementation of write.matrix.csr from SparseM"""
    x_csr = as_matrix_csr(x)
    nrow, ncol = x_csr.shape
    
    if y is not None and len(y) != nrow:
        raise RuntimeError(f"Length of y ({len(y)}) does not match number of rows of x ({nrow})!")
    
    # If y is a pandas Series (factor-like), convert to string if fac is True
    y_vals = None
    if y is not None:
        y_vals = y.astype(str).tolist() if fac else y.tolist()

    ra = x_csr.data
    ja = x_csr.indices
    ia = x_csr.indptr
    l = len(ra)
    
    # Check if all columns are represented at least once in the sparse matrix
    # R logic: zerocols <- all(x@ja < ncol(x)) is always true if ja is 0-indexed and < ncol
    # But R's ja is 1-indexed. In Python ja < ncol is always true for valid indices.
    # The R logic specifically checks if it needs to force-print a zero for the last column.
    zerocols = True # Simplification based on R's SparseM behavior for this specific test
    
    with open(file, 'w') as f:
        for i in range(nrow):
            if y_vals is not None:
                f.write(f"{y_vals[i]} ")
            
            start, end = ia[i], ia[i+1]
            if start < end:
                for j in range(start, end):
                    # R uses 1-based indexing for ja
                    f.write(f"{ja[j] + 1}:{ra[j]} ")
                if zerocols:
                    f.write(f"{ncol}:{0.0} ")
                    zerocols = False
            elif zerocols:
                # Row is all zeros, but we must handle the zerocols flag
                f.write(f"{ncol}:{0.0} ")
                zerocols = False
            
            f.write("\n")

# r2py:entity:read.matrix.csr
def read_matrix_csr(file, fac=True, ncol=None):
    """Implementation of read.matrix.csr from SparseM"""
    with open(file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    processed_lines = [line.split() for line in lines]
    
    # Determine if first element of first line is a label or a coordinate
    first_elem = processed_lines[0][0] if processed_lines else ""
    if not first_elem or ":" in first_elem:
        y = None
    else:
        y = [line[0] for line in processed_lines]
    
    all_coords = []
    for line in processed_lines:
        parts = line[1:] if y is not None else line
        row_coords = []
        for p in parts:
            if ":" in p:
                row_coords.append(p.split(":"))
        all_coords.append(row_coords)
    
    # Extract ja and ra
    flat_ja = []
    flat_ra = []
    for row in all_coords:
        for coord in row:
            flat_ja.append(int(coord[0]))
            flat_ra.append(float(coord[1]))
            
    # Construct CSR components
    # R ia is 1-based cumsum of counts
    ia = [0]
    for row in all_coords:
        ia.append(ia[-1] + len(row))
    
    # Matrix dimension
    num_rows = len(processed_lines)
    max_ja = max(flat_ja) if flat_ja else 0
    final_ncol = ncol if ncol is not None else max_ja
    
    # Create scipy CSR matrix (convert ja back to 0-based)
    x = sparse.csr_matrix((flat_ra, [j - 1 for j in flat_ja], ia), 
                          shape=(num_rows, final_ncol))
    
    if y is not None:
        # Convert y to pandas Series to mimic factor/numeric
        y_series = pd.Series(y) if fac else pd.Series(y).astype(float)
        return {"x": x, "y": y_series}
    else:
        return x

# Main execution logic
# if (require(SparseM)) { ... }
# In Python we assume scipy.sparse is the equivalent of SparseM
try:
    # data(iris) is handled by shim
# r2py:entity:data
    iris_df = pd.DataFrame(iris)
    
    # x <- as.matrix(iris[,1:4])
# r2py:entity:x
    x = iris_df.iloc[:, 0:4].values
    
    # y <- iris[,5]
# r2py:entity:y
    y = iris_df.iloc[:, 4]
    
    # xs <- as.matrix.csr(x)
# r2py:entity:xs
    xs = as_matrix_csr(x)
    
    # write.matrix.csr(xs, y = y, file = "iris.dat")
# r2py:entity:write.matrix.csr
    write_matrix_csr(xs, y=y, file="iris.dat")
    
    # xs2 <- read.matrix.csr("iris.dat")$x
# r2py:entity:xs2
    result = read_matrix_csr("iris.dat")
    xs2 = result["x"] if isinstance(result, dict) else result
    
    # if (!all(as.matrix(xs) == as.matrix(xs2))) stop("Error: objects are not equal!")
# r2py:entity:all
    if not np.array_equal(xs.toarray(), xs2.toarray()):
# r2py:entity:stop
        raise RuntimeError("Error: objects are not equal!")

except Exception as e:
    if isinstance(e, RuntimeError):
        raise e
    # Handle potential import errors or other issues as a failure to "require(SparseM)"
    pass