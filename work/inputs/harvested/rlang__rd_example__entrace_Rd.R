# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: entrace.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 11

suppressPackageStartupMessages(library(rlang))
quote({  # Not run

# Set `entrace()` globally in your RProfile
globalCallingHandlers(error = rlang::entrace)

# On older R versions which don't feature `globalCallingHandlers`,
# set the error handler like this:
options(error = rlang::entrace)

})