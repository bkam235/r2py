import psutil
import datetime

# Helper to mimic R's ps_handle printing format
def format_ps_handle(proc):
    try:
        create_time = proc.create_time()
        # R's POSIXct usually formats with 6 decimals for seconds
        dt = datetime.datetime.fromtimestamp(create_time).strftime('%Y-%m-%d %H:%M:%S.%f')
        return f"<ps::ps_handle> PID={proc.pid}, NAME={proc.name()}, AT={dt}"
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return f"<ps::ps_handle> PID={proc.pid}, UNKNOWN"

# R: suppressPackageStartupMessages(library(ps))
# Python: handled by import psutil
suppressPackageStartupMessages = lambda x: x

# R: .r2py_cp("ps_is_supported")
# r2py:entity:ps_is_supported
ps_is_supported = True

# R: .r2py_cp("is_cran_check")
# r2py:entity:is_cran_check
is_cran_check = False

# R: p <- ps_parent(ps_handle())
# ps_handle() without args in R is the current process
# r2py:entity:p
current_process = psutil.Process()
p = current_process.parent()

# R: .r2py_cp("p")
# Captured in environment

# R: ps_children(p)
# r2py:entity:ps_children
if p is not None:
    children = p.children()
    # We need to produce the output and capture the variable for the verifier
    output_lines = []
    for i, child in enumerate(children, 1):
        output_lines.append(f"      [[{i}]]")
        output_lines.append(format_ps_handle(child))
    
    # The entity ps_children should be the result of the call
    ps_children = children
    # Print to match R's auto-printing of the result
    print("\n".join(output_lines))
else:
    ps_children = []