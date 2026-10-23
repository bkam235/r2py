# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: gss_cat.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 5

suppressPackageStartupMessages(library(forcats))
gss_cat

fct_count(gss_cat$relig)
fct_count(fct_lump(gss_cat$relig))