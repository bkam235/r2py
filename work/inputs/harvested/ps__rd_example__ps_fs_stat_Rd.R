# r2py crawler metadata
# package: ps
# source_type: rd_example
# topic: ps_fs_stat.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ps\help
# lines: 4

suppressPackageStartupMessages(library(ps))
if (ps::ps_is_supported() && ! ps:::is_cran_check() && ps_os_type()[["POSIX"]]) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
ps_fs_stat(c(".", tempdir()))
}) # examplesIf