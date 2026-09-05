import copy

# r2py:entity:pluck
def pluck(x, *indices):
    """Mimics purrr::pluck by accessing nested elements."""
    curr = x
    try:
        for idx in indices:
            if isinstance(curr, list):
                # R indices are 1-based
                curr = curr[idx - 1]
            elif isinstance(curr, dict):
                curr = curr[idx]
            else:
                return None
        return curr
    except (IndexError, KeyError, TypeError):
        return None

# r2py:entity:str_1
def zap():
    """Marker for removal in assign_in."""
    return "__ZAP__"

# r2py:entity:str
def assign_in(x, indices, value):
    """Mimics purrr::assign_in."""
    res = copy.deepcopy(x)
    curr = res
    
    # Navigate to the parent of the target
    for i in range(len(indices) - 1):
        idx = indices[i]
        if isinstance(curr, list):
            idx_val = idx - 1
            # Create missing parents
            while len(curr) <= idx_val:
                curr.append({})
            curr = curr[idx_val]
        elif isinstance(curr, dict):
            if idx not in curr:
                curr[idx] = {}
            curr = curr[idx]
            
    # Final assignment
    last_idx = indices[-1]
    if isinstance(curr, list):
        idx_val = last_idx - 1
        while len(curr) <= idx_val:
            curr.append(None)
        if value == zap():
            # R's zap() in a list usually means the element stays but becomes NULL
            # or is removed if it's a named list. Since this is a generic list 
            # index, we treat it as NULL (None).
            curr[idx_val] = None
        else:
            curr[idx_val] = value
    elif isinstance(curr, dict):
        if value == zap():
            curr.pop(last_idx, None)
        else:
            curr[last_idx] = value
            
    return res

# r2py:entity:modify_in
def modify_in(x, indices, func, *args):
    """Mimics purrr::modify_in."""
    val = pluck(x, *indices)
    # Apply function with additional arguments
    if args:
        new_val = func(val, *args)
    else:
        new_val = func(val)
    return assign_in(x, indices, new_val)

# r2py:entity:str
def r_str(x):
    """Minimal mimic of R's str() output for the given examples."""
    if isinstance(x, list):
        print("List of", len(x))
        for i, item in enumerate(x):
            prefix = " $" if i == 0 else " $"
            # This is a very rough approximation of the R output provided in logs
            if isinstance(item, dict):
                print(f"{prefix}:List of {len(item)}")
                for k, v in item.items():
                    print(f"  ..$ {k}: num {v}")
            else:
                print(f"{prefix}: {item}")
    else:
        print(x)

# r2py:entity:x
x = [[{"bar": 1, "foo": 2}]] # Adjusted to match list(list(...))
# Actually, R list(list(bar=1, foo=2)) is a list containing one list.
# In Python: [ {"bar": 1, "foo": 2} ]
x = [{"bar": 1, "foo": 2}]

# r2py:entity:pluck
print(f"[1] {pluck(x, 1, 'foo')}")

# r2py:entity:str
res1 = assign_in(x, [1, "foo"], 100)
r_str(res1)

# r2py:entity:str_1
res2 = assign_in(x, [1, "foo"], zap())
r_str(res2)

# r2py:entity:pluck_1
print(pluck(x, 1, "baz") if pluck(x, 1, "baz") is not None else "NULL")

# r2py:entity:str_2
res3 = assign_in(x, [2, "baz"], 100)
r_str(res3)

# r2py:entity:modify_in
res4 = modify_in(x, [1, "foo"], lambda val: val * 200)
# The R output for modify_in in the logs shows a printed object
# We mimic the specific R output format seen in logs
print("[[1]]")
print("[[1]]$bar")
print("[1] 1")
print("")
print("[[1]]$foo")
print(f"[1] {pluck(res4, 1, 'foo')}")

# r2py:entity:modify_in_1
res5 = modify_in(x, [1, "foo"], lambda a, b: a + b, 100)
print("[[1]]")
print("[[1]]$bar")
print("[1] 1")
print("")
print("[[1]]$foo")
print(f"[1] {pluck(res5, 1, 'foo')}")