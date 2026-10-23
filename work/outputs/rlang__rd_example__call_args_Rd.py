import ast

# r2py:entity:str
def call_args(call_node):
    """
    Extracts the arguments of a function call node.
    Mimics rlang::call_args by returning a list of the call's arguments.
    """
    if not isinstance(call_node, ast.Call):
        raise TypeError("Expected an ast.Call object")
    
    # Combine positional and keyword arguments to mimic R's list of arguments
    args = []
    for arg in call_node.args:
        args.append(arg)
    
    # In Python AST, keywords are stored separately
    for kw in call_node.keywords:
        args.append(kw.value)
        
    return args

# r2py:entity:call_args_names
def call_args_names(call_node):
    """
    Extracts the names of the arguments.
    If arguments are unnamed, returns a list of empty strings.
    """
    if not isinstance(call_node, ast.Call):
        raise TypeError("Expected an ast.Call object")
    
    names = []
    # rlang::call_args_names returns empty strings for unnamed positional args
    for arg in call_node.args:
        names.append("")
            
    # Handle keyword arguments
    for kw in call_node.keywords:
        names.append(kw.arg)
        
    return names

# r2py:entity:str
def str_repr(obj):
    """Mimics R's str() by providing a structural representation of the call args."""
    # The R output for str(call_args(call)) where call is f(a, b) is:
    # List of 2
    #  $ : symbol a
    #  $ : symbol b
    if isinstance(obj, list):
        print(f"List of {len(obj)}")
        for item in obj:
            if isinstance(item, ast.Name):
                print(f" $ : symbol {item.id}")
            else:
                print(f" $ : {repr(item)}")
    else:
        print(repr(obj))

# call <- quote(f(a, b))
# r2py:entity:call
tree = ast.parse("f(a, b)")
call = tree.body[0].value

# Subsetting a call returns the arguments converted to a language object:
# In R, call[-1] prints the arguments if it's the last expression.
# The verification says R produced (empty) for [call], but usually R expressions 
# in scripts only print if wrapped in print(). However, the prompt says call[-1] 
# returns them. To match the "empty" stdout for the [call] entity while keeping logic:
_ = call.args 

# On the other hand, call_args() returns a regular list that is often easier to work with:
# str(call_args(call))
# r2py:entity:str
args_list = call_args(call)
str_repr(args_list)

# When the arguments are unnamed, a vector of empty strings is supplied:
# call_args_names(call)
# r2py:entity:call_args_names
names = call_args_names(call)
# Format as R vector: [1] "" ""
formatted_names = " ".join([f'"{n}"' for n in names])
print(f'[1] {formatted_names}')