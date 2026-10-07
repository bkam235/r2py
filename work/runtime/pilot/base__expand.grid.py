import numpy as np
import pandas as pd

def r_expand_grid(*args, KEEP_OUT_ATTRS=True, stringsAsFactors=True, **kwargs):
    # R's expand.grid handles ... as the primary input.
    # In Python, if the user passes named arguments via kwargs, they are part of the grid.
    # If they pass positional args, those are also part of the grid.
    
    # Combine positional and keyword arguments into a list of pairs (name, value)
    all_args = []
    
    # First, handle positional arguments
    for i, val in enumerate(args):
        # The R function handles a single list argument as the input set
        # But in Python, we typically expect the grid components as separate arguments
        all_args.append(val)
    
    # Then handle keyword arguments, but exclude the control parameters
    control_params = {'KEEP_OUT_ATTRS', 'stringsAsFactors'}
    kw_args = {k: v for k, v in kwargs.items() if k not in control_params}
    
    # If the user provided a single list/dict as the first positional arg, 
    # and no other positional/keyword args, R's logic replaces the arg list.
    # However, the typical use case is passed directly.
    
    # To mimic R's `...` behavior:
    # 1. Collect all items intended for the grid.
    # 2. Determine names.
    
    grid_inputs = []
    input_names = []
    
    # R's `...` includes positional args. 
    # If the first arg is a list, and it's the only arg, it's treated as the list of inputs.
    if len(args) == 1 and isinstance(args[0], (list, dict)):
        if isinstance(args[0], dict):
            for k, v in args[0].items():
                input_names.append(k)
                grid_inputs.append(v)
        else:
            # Treat list as a set of unnamed inputs
            for v in args[0]:
                grid_inputs.append(v)
    else:
        # Standard behavior: positional args first, then named kwargs
        for i, val in enumerate(args):
            grid_inputs.append(val)
            input_names.append(f"Var{i+1}")
        
        for k, v in kw_args.items():
            grid_inputs.append(v)
            input_names.append(k)

    # Correct names: if kwargs were used, they override the VarX pattern for those specific args
    # In R, if names(...) is not null, it uses them.
    # Since Python positional args don't have names, we use Var1, Var2...
    # But if we have a mix, the kwargs names are preserved.
    
    # Re-evaluating the name logic to match R exactly:
    # The positional args get Var1, Var2... 
    # If the user called expand.grid(a=1, b=2), the names are 'a', 'b'.
    
    # Let's refine the input collection:
    final_inputs = []
    final_names = []
    
    # All positional args
    for i, val in enumerate(args):
        final_inputs.append(np.atleast_1d(val))
        final_names.append(f"Var{i+1}")
    
    # All keyword args (excluding control)
    for k, v in kw_args.items():
        final_inputs.append(np.atleast_1d(v))
        final_names.append(k)

    nargs = len(final_inputs)
    if nargs == 0:
        return pd.DataFrame()

    # Calculate dimensions
    d = [len(x) for x in final_inputs]
    orep = np.prod(d, dtype=int)

    if orep == 0:
        # Return empty dataframe with correct columns
        return pd.DataFrame({name: [] for name in final_names})

    result_dict = {}
    rep_fac = 1
    
    for i in range(nargs):
        x = final_inputs[i]
        nx = len(x)
        
        # R logic: 
        # x <- x[rep.int(rep.int(seq_len(nx), rep.int(rep_fac, nx)), orep)]
        # This is essentially a tiling operation.
        # Current rep_fac is the product of lengths of previous dimensions.
        # We need to repeat each element of x, rep_fac times, 
        # and then tile that whole block to fill orep.
        
        # Python equivalent:
        # 1. Repeat each element rep_fac times: [1, 1, 2, 2]
        # 2. Tile the result until total length is orep.
        
        # However, R's expand.grid expands the FIRST variable fastest.
        # Var1: 1, 2, 1, 2
        # Var2: A, A, B, B
        # This means Var1 cycles, then Var2 stays constant for the length of Var1's cycle.
        
        # Correct pattern for Var i:
        # Each element is repeated rep_fac times.
        # Then the sequence is tiled (orep // (nx * rep_fac)) times.
        
        # Wait, the R code: x[rep.int(rep.int(seq_len(nx), rep.int(rep_fac, nx)), orep)]
        # Let's trace:
        # i=1: nx=2, rep_fac=1. rep.int(1:2, 1) -> 1,2. rep.int(1,2, orep) -> 1,2,1,2...
        # i=2: nx=2, rep_fac=2. rep.int(1:2, 2) -> 1,1,2,2. rep.int(1,1,2,2, orep) -> 1,1,2,2...
        
        # In numpy:
        # Tile the array, then repeat elements.
        # No, that's not it.
        # The R code `rep.int(seq_len(nx), rep.int(rep_fac, nx))` is actually
        # `rep(1:nx, each = rep_fac)`.
        # Then it tiles that block.
        
        block = np.repeat(x, rep_fac)
        full_col = np.tile(block, orep // len(block))
        
        # Handle stringsAsFactors
        if stringsAsFactors and isinstance(x[0], str):
            # In R, factor is returned as strings in this Python reproduction
            pass
            
        result_dict[final_names[i]] = full_col
        rep_fac *= nx

    return pd.DataFrame(result_dict)
