# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: J.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 17

suppressPackageStartupMessages(library(data.table))
DT = data.table(A=5:1, B=letters[5:1])
setkey(DT, B)   # reorders table and marks it sorted
DT[J("b")]      # returns the 2nd row
DT[list("b")]   # same
DT[.("b")]      # same using the dot alias for list

# CJ usage examples
CJ(c(5, NA, 1), c(1, 3, 2))                 # sorted and keyed data.table
do.call(CJ, list(c(5, NA, 1), c(1, 3, 2)))  # same as above
CJ(c(5, NA, 1), c(1, 3, 2), sorted=FALSE)   # same order as input, unkeyed
# use for 'unique=' argument
x = c(1, 1, 2)
y = c(4, 6, 4)
CJ(x, y)              # output columns are automatically named 'x' and 'y'
CJ(x, y, unique=TRUE) # unique(x) and unique(y) are computed automatically
CJ(x, y, sorted = FALSE) # retain input order for y