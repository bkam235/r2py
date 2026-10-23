# r2py crawler metadata
# package: ps
# source_type: rd_example
# topic: ps_connections.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ps\help
# lines: 9

suppressPackageStartupMessages(library(ps))
if (ps::ps_is_supported() && ! ps:::is_cran_check()) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
p <- ps_handle()
ps_connections(p)
sc <- socketConnection("httpbin.org", port = 80)
ps_connections(p)
close(sc)
ps_connections(p)
}) # examplesIf