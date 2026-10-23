# r2py crawler metadata
# package: callr
# source_type: rd_example
# topic: rcmd_process.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\callr\help
# lines: 7

suppressPackageStartupMessages(library(callr))
if (FALSE) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
options <- rcmd_process_options(cmd = "config", cmdargs = "CC")
rp <- rcmd_process$new(options)
rp$wait()
rp$read_output_lines()
}) # examplesIf