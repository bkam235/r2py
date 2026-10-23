# r2py crawler metadata
# package: pillar
# source_type: rd_example
# topic: type_sum.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\help
# lines: 11

suppressPackageStartupMessages(library(pillar))
obj_sum(1:10)
obj_sum(matrix(1:10))
obj_sum(data.frame(a = 1))
obj_sum(Sys.Date())
obj_sum(Sys.time())
obj_sum(mean)

size_sum(1:10)
size_sum(trees)
size_sum(Titanic)