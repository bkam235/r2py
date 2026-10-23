# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: tibble_s14
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\tibble.R
# lines: 9

suppressPackageStartupMessages(library(tibble))
df <- data.frame(a = 1:3, row.names = letters[1:3])
rownames(df)
rownames(as_tibble(df))

tbl <- tibble(a = 1:3)
rownames(tbl) <- letters[1:3]
rownames(tbl)
rownames(tbl[1, ])