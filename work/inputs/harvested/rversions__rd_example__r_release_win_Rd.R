# r2py crawler metadata
# package: rversions
# source_type: rd_example
# topic: r_release_win.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rversions\help
# lines: 5

suppressPackageStartupMessages(library(rversions))
if (rversions:::is_online()) withAutoprint({ # examplesIf
r_release()
r_release_win()
}) # examplesIf