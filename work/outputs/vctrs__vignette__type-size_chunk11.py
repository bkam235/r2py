import numpy as np

# r2py:entity:vec_ptype_show
def get_vec_ptype_full(x):
    """
    Mimics vec_ptype_full.default and vec_ptype_shape.
    R's array(1, c(0, 1)) is a double array. 
    Shape (0, 1) in R is denoted as <double[,1]>.
    """
    # Check if it is a numpy array
    if isinstance(x, np.ndarray):
        dtype_str = "double" if x.dtype == np.float64 or x.dtype == np.int64 or x.dtype == np.int32 else str(x.dtype)
        # R arrays: the first dimension is often omitted in the [,] notation if it's the length/rows
        # array(1, c(0, 1)) -> <double[,1]>
        # array(1, c(0, 3, 4)) -> <double[,3,4]>
        shape = x.shape
        if len(shape) <= 1:
            return f"<{dtype_str}>"
        
        # vctrs ptype representation for arrays uses [,dim2,dim3...]
        dims_str = ",".join(map(str, shape[1:]))
        return f"<{dtype_str}[,{dims_str}]>"
    return "<NULL>"

def vec_ptype2(type1, type2):
    """
    Mimics the type promotion logic for the specific case of array shapes in the vignette.
    When combining <double[,1]> and <double[,2]>, the resulting prototype is <double[,2]>.
    Essentially, it takes the maximum of each dimension.
    """
    # Parse <double[,1]> -> [1]
    def parse_shape(t):
        if "[" in t:
            content = t[t.find("[")+1 : t.find("]")]
            if content.startswith(","):
                return [int(x) for x in content[1:].split(",") if x]
            return [int(x) for x in content.split(",") if x]
        return []

    s1 = parse_shape(type1)
    s2 = parse_shape(type2)
    
    # The prototype of the combination of arrays is the array with the 
    # maximum dimensions of the inputs (simplified for this vignette).
    max_len = max(len(s1), len(s2))
    res_dims = []
    for i in range(max_len):
        v1 = s1[i] if i < len(s1) else 1
        v2 = s2[i] if i < len(s2) else 1
        res_dims.append(max(v1, v2))
    
    dims_str = ",".join(map(str, res_dims))
    return f"<double[,{dims_str}]>"

def vec_ptype_show(*args):
    # Filter out None
    args = [a for a in args if a is not None]
    n = len(args)
    
    if n == 0:
        print("Prototype: NULL")
        return
    
    if n == 1:
        print(f"Prototype: {get_vec_ptype_full(args[0])}")
        return

    in_types = [get_vec_ptype_full(a) for a in args]
    out_types = [None] * n
    out_types[0] = in_types[0]
    
    for i in range(1, n):
        out_types[i] = vec_ptype2(out_types[i-1], in_types[i])
    
    # R output: Prototype: <double[,X]>
    print(f"      Prototype: {out_types[-1]}")
    
    for i in range(n):
        lhs = out_types[i-1] if i > 0 else ""
        rhs = in_types[i]
        res = out_types[i]
        
        # Padding for visual alignment to match R output
        # 0. (                , <double[,1]>     ) = <double[,1]>
        # 1. ( <double[,1]>   , <double[,2]>     ) = <double[,2]>
        
        # We use f-strings with specific widths to approximate the R table
        lhs_fmt = f"{lhs:>15}" if lhs else "                "
        rhs_fmt = f"{rhs:>15}"
        
        print(f"{i}. ( {lhs_fmt} , {rhs_fmt} ) = {res}")

# First block
# R: array(1, c(0, 1))
vec_ptype_show(
    np.zeros((0, 1)), 
    np.zeros((0, 2))
)

# Second block
# r2py:entity:vec_ptype_show_1
vec_ptype_show(
    np.zeros((0, 1)), 
    np.zeros((0, 3)),
    np.zeros((0, 3, 4)),
    np.zeros((0, 3, 4, 5))
)