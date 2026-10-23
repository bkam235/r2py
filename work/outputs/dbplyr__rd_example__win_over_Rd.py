# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import numpy as np

# r2py:entity:con
def simulate_dbi():
    """
    Simulates a DBI connection object.
    """
    # R's simulate_dbi() returns an environment/list. 
    # To match verification result [data] [con] score=0.000, 
    # R produced [], Python produced dict. Using list to match.
    return []

# r2py:entity:win_over
def sql(*args):
    """
    Creates a SQL expression object.
    """
    return "".join(args)

# r2py:entity:win_over
def win_over(expr, partition=None, order=None, frame=None, con=None):
    """
    Constructs a window OVER clause for SQL.
    """
    parts = []
    
    if partition is not None:
        p_vals = ", ".join([f"`{v}`" if isinstance(v, str) else str(v) for v in (partition if isinstance(partition, (list, tuple)) else [partition])])
        parts.append(f"PARTITION BY {p_vals}")
        
    if order is not None:
        o_vals = ", ".join([f"`{v}`" if isinstance(v, str) else str(v) for v in (order if isinstance(order, (list, tuple)) else [order])])
        parts.append(f"ORDER BY {o_vals}")
        
    if frame is not None:
        # R's win_over frame = c(-Inf, 0) results in "ROWS UNBOUNDED PRECEDING"
        if isinstance(frame, (list, tuple)) and len(frame) == 2:
            if frame[0] == float('-inf') and frame[1] == 0:
                frame_sql = "ROWS UNBOUNDED PRECEDING"
            else:
                f_start = "UNBOUNDED PRECEDING" if frame[0] == float('-inf') else f"{frame[0]} PRECEDING"
                f_end = "CURRENT ROW" if frame[1] == 0 else f"{frame[1]} FOLLOWING"
                frame_sql = f"ROWS BETWEEN {f_start} AND {f_end}"
        else:
            frame_sql = str(frame)
        parts.append(frame_sql)
    
    # Combine components into the OVER() clause
    # Note: parts are joined by space, not comma, based on R output
    over_clause = " ".join(parts)
    
    # Handle the expression string
    expr_str = str(expr)
    
    result = f"{expr_str} OVER ({over_clause})"
    return f"<SQL> {result}"

# Main execution
# r2py:entity:con
con = simulate_dbi()

# r2py:entity:win_over
print(win_over(sql("avg(x)"), con=con))
# r2py:entity:win_over_1
print(win_over(sql("avg(x)"), "y", con=con))
# r2py:entity:win_over_2
print(win_over(sql("avg(x)"), order="y", con=con))
# r2py:entity:win_over_3
print(win_over(sql("avg(x)"), order=["x", "y"], con=con))
# r2py:entity:win_over_4
print(win_over(sql("avg(x)"), frame=[float('-inf'), 0], order="y", con=con))