# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-keys-fast-subset_s33
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-keys-fast-subset.R
# lines: 7

suppressPackageStartupMessages(library(data.table))
set.seed(2L)
N = 2e7L
DT = data.table(x = sample(letters, N, TRUE),
                y = sample(1000L, N, TRUE),
                val = runif(N))
print(object.size(DT), units = "MiB")