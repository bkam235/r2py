# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: fsort.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 5

suppressPackageStartupMessages(library(data.table))
x = runif(1e6)
system.time(ans1 <- sort(x, method="quick"))
system.time(ans2 <- fsort(x))
identical(ans1, ans2)