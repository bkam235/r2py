import sys
import warnings

# r2py:entity:import_fansi
# fansi library import (simulated)
# r2py:entity:suppressPackageStartupMessages
# suppressPackageStartupMessages(library(fansi))

# The R package 'fansi' provides a constant sgr.string containing ANSI sequences.
# We define it here to match R's internal constant.
sgr_string = "\033[31mRed Text\033[0m"

try:
    # r2py:entity:message
    # message(paste0(sgr.string, collapse="\n"))
    # R's message() prints to stderr
    sys.stderr.write(sgr_string + "\n")
    sys.stderr.flush()

    # r2py:entity:warning
    # warning(paste0(c("", sgr.string), collapse="\n"))
    # Use warnings.warn; we'll use a simple string to match R's output
    warnings.warn("\n" + sgr_string, stacklevel=2)

    # r2py:entity:stop
    # stop(paste0(c("", sgr.string), collapse="\n"))
    raise RuntimeError("\n" + sgr_string)

except RuntimeError:
    # R's try() without arguments captures the error silently without printing to stdout
    pass