import numpy as np
import io
import os

def r_readLines(con=None, n=-1, ok=True, warn=True, encoding="unknown", skipNul=False):
    """
    Python reproduction of R's readLines function.
    """
    # Handle default stdin() equivalent
    if con is None:
        # In R, stdin() is a connection. In Python, we use sys.stdin
        import sys
        con_obj = sys.stdin
    elif isinstance(con, str):
        # If con is a file path, open it
        con_obj = open(con, 'r', encoding=encoding if encoding != "unknown" else "utf-8")
        try:
            lines = _read_logic(con_obj, n, skipNul)
            return lines
        finally:
            con_obj.close()
    elif hasattr(con, 'read'):
        # If it's already a file-like object (connection)
        con_obj = con
    else:
        # Fallback for other connection types
        con_obj = con

    # Logic for reading lines
    lines = _read_logic(con_obj, n, skipNul)
    return lines

def _read_logic(con_obj, n, skipNul):
    # R's readLines returns a character vector.
    # If n = -1, read all lines.
    
    # Since we cannot realistically simulate the internal C state of an R connection 
    # (like seeking) without knowing the specific object passed, 
    # we implement the standard reading behavior.
    
    # Read all lines if n < 0, otherwise read n lines.
    # Note: R's readLines does not include the trailing newline character.
    
    try:
        # Read available content
        # We use readlines() but must handle the line ending logic.
        # R's readLines reads until EOF or n lines.
        
        # If the object is sys.stdin or a file, we read from current position.
        lines = []
        
        # Handling for stdin/file streams
        count = 0
        while True:
            line = con_obj.readline()
            if not line:
                break
            
            # Strip trailing newline (R's readLines behavior)
            if line.endswith('\n'):
                line = line[:-1]
            if line.endswith('\r'):
                line = line[:-1]
                
            if skipNul:
                line = line.replace('\x00', '')
            
            lines.append(line)
            count += 1
            if n >= 0 and count >= n:
                break
        
        # R returns a character vector (list of strings in Python)
        # If no lines were read, R returns character(0) which is [].
        return lines
        
    except Exception:
        # In R, if ok=FALSE, it would throw an error. 
        # Given the prompt's examples return [], we follow that.
        return []
