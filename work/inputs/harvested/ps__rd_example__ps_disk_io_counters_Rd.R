# r2py crawler metadata
# package: ps
# source_type: rd_example
# topic: ps_disk_io_counters.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ps\help
# lines: 4

suppressPackageStartupMessages(library(ps))
if (ps::ps_is_supported() && ps:::ps_os_name() %in% c("LINUX", "WINDOWS") && !ps:::is_cran_check()) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
ps_disk_io_counters()
}) # examplesIf