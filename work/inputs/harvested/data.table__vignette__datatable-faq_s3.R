# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-faq_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-faq.R
# lines: 9

suppressPackageStartupMessages(library(data.table))
X = data.table(grp = c("a", "a", "b",
                       "b", "b", "c", "c"), foo = 1:7)
setkey(X, grp)
Y = data.table(c("b", "c"), bar = c(4, 2))
X
Y
X[Y, sum(foo*bar)]
X[Y, sum(foo*bar), by = .EACHI]