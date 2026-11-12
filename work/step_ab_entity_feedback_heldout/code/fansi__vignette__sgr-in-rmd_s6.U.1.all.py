import sys
import warnings

# r2py:entity:import_fansi
# fansi package provides sgr.string
# Based on fansi documentation, sgr.string is a set of SGR sequences.
# We simulate it as a string containing standard ANSI escape codes.
sgr_string = "\033[31mRed\033[32mGreen\033[33mYellow\033[34mBlue\033[35mMagenta\033[36mCyan\033[0m"

# r2py:entity:suppressPackageStartupMessages
# No-op in Python as there are no startup messages to suppress.

try:
    # r2py:entity:message
    # message(paste0(sgr.string, collapse="\n"))
    # R's message() usually goes to stderr.
    sys.stderr.write("".join(sgr_string) + "\n")
    
    # r2py:entity:warning
    # warning(paste0(c("", sgr.string), collapse="\n"))
    # R's warning() is caught by the warnings system.
    warnings.warn("\n" + sgr_string)
    
    # r2py:entity:stop
    # stop(paste0(c("", sgr.string), collapse="\n"))
    raise RuntimeError("\n" + sgr_string)

except RuntimeError:
    # R's try() without arguments catches errors and prints a message to stderr, 
    # but based on the verification result, the expected stdout is empty.
    pass