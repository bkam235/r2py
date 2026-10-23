# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-reshape_s18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-reshape.R
# lines: 4

suppressPackageStartupMessages(library(data.table))
(who <- data.table(id=1, new_sp_m5564=2, newrel_f65=3))
melt(who, measure.vars = measure(
  diagnosis, gender, ages, pattern="new_?(.*)_(.)(.*)"))