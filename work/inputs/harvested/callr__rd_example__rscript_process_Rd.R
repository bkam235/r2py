# r2py crawler metadata
# package: callr
# source_type: rd_example
# topic: rscript_process.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\callr\help
# lines: 7

suppressPackageStartupMessages(library(callr))
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
options <- rscript_process_options(script = "script.R")
rp <- rscript_process$new(options)
rp$wait()
rp$read_output_lines()
}) # examplesIf