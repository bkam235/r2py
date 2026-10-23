# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: fdroplevels.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 15

suppressPackageStartupMessages(library(data.table))
# on vectors
x = factor(letters[1:10])
fdroplevels(x[1:5])
# exclude levels from drop
fdroplevels(x[1:5], exclude = c("a", "c"))

# on data.table
DT = data.table(a = factor(1:10), b = factor(letters[1:10]))
droplevels(head(DT))[["b"]]
# exclude levels
droplevels(head(DT), exclude = c("b", "c"))[["b"]]
# except columns from drop
droplevels(head(DT), except = 2)[["b"]]
droplevels(head(DT), except = 1)[["b"]]