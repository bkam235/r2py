import sys
import warnings

# r2py:entity:import_fansi
# fansi provides sgr.string which is a vector of SGR sequences.
# Based on fansi documentation, sgr.string is used for testing SGR processing.
sgr_string = "\033[31mRed\033[0m\n\033[32mGreen\033[0m\n\033[33mYellow\033[0m"

# r2py:entity:suppressPackageStartupMessages
# No-op in Python

try:
    # r2py:entity:message
    # message(paste0(sgr.string, collapse="\n"))
    # R's message() typically prints to stderr.
    sys.stderr.write(sgr_string + "\n")
    
    # r2py:entity:warning
    # warning(paste0(c("", sgr.string), collapse="\n"))
    warnings.warn("\n" + sgr_string)
    
    # r2py:entity:stop
    # stop(paste0(c("", sgr.string), collapse="\n"))
    raise Exception("\n" + sgr_string)

except Exception:
    # R's try() without an expr argument suppresses the error output 
    # and returns the error object. We simply pass to mimic the behavior.
    pass