# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-reference-semantics_s25
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-reference-semantics.R
# lines: 15

suppressPackageStartupMessages(library(data.table))
DT = data.table(a = 1:3)

# three ways to get the column
x_ref = DT$a        # may be a reference
y_cpy = DT[, a]     # always a copy
z_cpy = copy(DT$a)  # forced copy

# modify DT by reference
DT[, a := a + 10L]

# observe results
x_ref   # may show 11 12 13
y_cpy   # 1 2 3
z_cpy   # 1 2 3