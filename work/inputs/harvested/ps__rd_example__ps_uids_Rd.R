# r2py crawler metadata
# package: ps
# source_type: rd_example
# topic: ps_uids.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ps\help
# lines: 7

suppressPackageStartupMessages(library(ps))
if (ps::ps_is_supported() && ps::ps_os_type()["POSIX"] && ! ps:::is_cran_check()) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
p <- ps_handle()
p
ps_uids(p)
ps_gids(p)
}) # examplesIf