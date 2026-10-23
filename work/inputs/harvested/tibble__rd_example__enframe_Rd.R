# r2py crawler metadata
# package: tibble
# source_type: rd_example
# topic: enframe.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\help
# lines: 7

suppressPackageStartupMessages(library(tibble))
enframe(1:3)
enframe(c(a = 5, b = 7))
enframe(list(one = 1, two = 2:3, three = 4:6))
deframe(enframe(3:1))
deframe(tibble(a = 1:3))
deframe(tibble(a = as.list(1:3)))