# r2py crawler metadata
# package: ps
# source_type: rd_example
# topic: ps_open_files.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ps\help
# lines: 10

suppressPackageStartupMessages(library(ps))
if (ps::ps_is_supported() && ! ps:::is_cran_check()) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
p <- ps_handle()
ps_open_files(p)
f <- file(tmp <- tempfile(), "w")
ps_open_files(p)
close(f)
unlink(tmp)
ps_open_files(p)
}) # examplesIf