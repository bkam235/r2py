# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-secondary-indices-and-auto-indexing_s25
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-secondary-indices-and-auto-indexing.R
# lines: 4

suppressPackageStartupMessages(library(data.table))
set.seed(1L)
dt = data.table(x = sample(1e5L, 1e7L, TRUE), y = runif(100L))
print(object.size(dt), units = "Mb")