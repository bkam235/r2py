# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import sys
import warnings

# r2py:entity:import_fansi
# fansi is used for SGR string manipulation. 
# sgr.string in R is a predefined vector of SGR sequences.
# We approximate this constant here.
sgr_string = "\033[31mRed Text\033[0m" 

# r2py:entity:suppressPackageStartupMessages
# No-op in Python

try:
    # r2py:entity:message
    # message(paste0(sgr.string, collapse="\n"))
    # In R, message() prints to stderr
    sys.stderr.write(sgr_string + "\n")
    
    # r2py:entity:warning
    # warning(paste0(c("", sgr.string), collapse="\n"))
    # R's paste0(c("", sgr.string), collapse="\n") results in "\n" + sgr.string
    warnings.warn("\n" + sgr_string)
    
    # r2py:entity:stop
    # stop(paste0(c("", sgr.string), collapse="\n"))
    raise RuntimeError("\n" + sgr_string)

except RuntimeError:
    # try() in R catches the error silently unless echo=TRUE
    pass