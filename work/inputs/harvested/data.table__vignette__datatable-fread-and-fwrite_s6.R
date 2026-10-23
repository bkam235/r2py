# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-fread-and-fwrite_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-fread-and-fwrite.R
# lines: 4

suppressPackageStartupMessages(library(data.table))
# fread's default behavior is to treat large integers as "integer64"; however, this global setting can be changed:
options(datatable.integer64 = "double")   # Example: set globally to "double"
getOption("datatable.integer64")