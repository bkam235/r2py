# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-keys-fast-subset_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-keys-fast-subset.R
# lines: 10

suppressPackageStartupMessages(library(data.table))
set.seed(1L)
DF = data.frame(ID1 = sample(letters[1:2], 10, TRUE),
                ID2 = sample(1:3, 10, TRUE),
                val = sample(10),
                stringsAsFactors = FALSE,
                row.names = sample(LETTERS[1:10]))
DF

rownames(DF)