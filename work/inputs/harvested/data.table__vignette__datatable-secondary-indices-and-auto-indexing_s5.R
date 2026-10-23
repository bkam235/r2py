# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-secondary-indices-and-auto-indexing_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-secondary-indices-and-auto-indexing.R
# lines: 4

suppressPackageStartupMessages(library(data.table))
DT = data.table(a = c(TRUE, FALSE), b = 1:2)
setkey(DT, a)                # Set key, reordering DT
DT[.(TRUE)]                  # 'on' is optional; if omitted, the key is used