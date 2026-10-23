# r2py crawler metadata
# package: ps
# source_type: rd_example
# topic: ps_get_cpu_affinity.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ps\help
# lines: 14

suppressPackageStartupMessages(library(ps))
if (ps::ps_is_supported() && ! ps:::is_cran_check() && ! ps::ps_os_type()[["MACOS"]]) (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
# current
orig <- ps_get_cpu_affinity()
orig

# restrict
ps_set_cpu_affinity(affinity = 0:0)
ps_get_cpu_affinity()

# restore
ps_set_cpu_affinity(affinity = orig)
ps_get_cpu_affinity()
}) # examplesIf