# r2py crawler metadata
# package: callr
# source_type: rd_example
# topic: r_process.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\callr\help
# lines: 11

suppressPackageStartupMessages(library(callr))
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
## List all options and their default values:
r_process_options()

## Start an R process in the background, wait for it, get result
opts <- r_process_options(func = function() 1 + 1)
rp <- r_process$new(opts)
rp$wait()
rp$get_result()
}) # examplesIf