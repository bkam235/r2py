# r2py crawler metadata
# package: ps
# source_type: rd_example
# topic: ps_children.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ps\help
# lines: 5

suppressPackageStartupMessages(library(ps))
if (ps::ps_is_supported() && ! ps:::is_cran_check()) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
p <- ps_parent(ps_handle())
ps_children(p)
}) # examplesIf