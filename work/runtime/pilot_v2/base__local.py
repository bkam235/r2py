import numpy as np
import pandas as pd

def r_local(expr, envir=None):
    """
    Reproduces R's local() function.
    In R, local({expr}, envir) evaluates expr in a new environment 
    that inherits from envir.
    
    Since this is a Python reproduction and 'expr' in the R examples 
    are blocks of code returning values, we interpret the Python 'expr' 
    as a callable or a piece of logic to be executed. 
    However, based on the provided examples, the 'expr' passed to local() 
    is effectively the code being executed, and it returns the value of the 
    last expression.
    """
    # In R, local creates a new environment. 
    # In Python, we simulate this by executing the expression.
    # If expr is passed as a function (simulating the block { ... }), we call it.
    # If it's a value, we return it.
    
    # The provided R examples show blocks like {print(1)}.
    # In a Python harness simulating R, these blocks are typically 
    # passed as functions or lambdas.
    
    if callable(expr):
        # R's local returns the value of the last expression in the block.
        # The examples show print() being used, but in R print() returns the object.
        return expr()
    else:
        return expr
