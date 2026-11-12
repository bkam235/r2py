import sys
import warnings

# r2py:entity:import_fansi
# r2py:entity:suppressPackageStartupMessages
# Simulating fansi::sgr.string constant
sgr_string = "\033[31mRed\033[0m\n\033[32mGreen\033[0m"

try:
    # r2py:entity:message
    # message(paste0(sgr.string, collapse="\n"))
    print(sgr_string, file=sys.stderr)
    
    # r2py:entity:warning
    # warning(paste0(c("", sgr.string), collapse="\n"))
    warnings.warn("\n" + sgr_string)
    
    # r2py:entity:stop
    # stop(paste0(c("", sgr.string), collapse="\n"))
    raise RuntimeError("\n" + sgr_string)

except Exception:
    # try() in R suppresses the error output and allows execution to continue
    pass