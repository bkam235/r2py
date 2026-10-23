# r2py crawler metadata
# package: ps
# source_type: rd_example
# topic: ps_shared_libs.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ps\help
# lines: 5

suppressPackageStartupMessages(library(ps))
if (ps::ps_is_supported() && ! ps:::is_cran_check() && ps::ps_os_type()[["WINDOWS"]]) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
# The loaded DLLs of the current process
ps_shared_libs()
}) # examplesIf