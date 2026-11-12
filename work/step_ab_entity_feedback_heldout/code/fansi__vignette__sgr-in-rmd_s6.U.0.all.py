import sys
import warnings

# Simulating the fansi package's sgr.string constant
# In R, sgr.string is a specific ANSI escape sequence provided by the fansi package.
sgr_string = "\033[31mRed Text\033[0m"

# suppressPackageStartupMessages(library(fansi))
# No startup messages to suppress in Python import.

try:
    # message(paste0(sgr.string, collapse="\n"))
    # R's message() prints to stderr.
    sys.stderr.write(sgr_string + "\n")
    sys.stderr.flush()

    # warning(paste0(c("", sgr.string), collapse="\n"))
    # c("", sgr.string) creates a vector of length 2, collapse="\n" puts a newline between them.
    warnings.warn("\n" + sgr_string)

    # stop(paste0(c("", sgr.string), collapse="\n"))
    raise RuntimeError("\n" + sgr_string)

except Exception:
    # R's try() without arguments suppresses the error output unless specifically handled.
    # To match R's behavior where it doesn't print "Caught exception...", we simply pass.
    pass