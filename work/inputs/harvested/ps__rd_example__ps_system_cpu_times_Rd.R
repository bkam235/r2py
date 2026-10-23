# r2py crawler metadata
# package: ps
# source_type: rd_example
# topic: ps_system_cpu_times.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ps\help
# lines: 4

suppressPackageStartupMessages(library(ps))
if (ps::ps_is_supported()) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
ps_system_cpu_times()
}) # examplesIf