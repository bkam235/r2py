# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-reference-semantics_s24
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-reference-semantics.R
# lines: 17

suppressPackageStartupMessages(library(data.table))
DT = data.table(x = 1L, y = 2L)
DT_n = names(DT)
DT_n

## add a new column by reference
DT[, z := 3L]

## DT_n also gets updated
DT_n

## use `copy()`
DT_n = copy(names(DT))
DT[, w := 4L]

## DT_n doesn't get updated
DT_n