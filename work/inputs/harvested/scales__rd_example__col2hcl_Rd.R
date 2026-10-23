# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: col2hcl.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 6

suppressPackageStartupMessages(library(scales))
reds <- rep("red", 6)
show_col(col2hcl(reds, h = seq(0, 180, length = 6)))
show_col(col2hcl(reds, c = seq(0, 80, length = 6)))
show_col(col2hcl(reds, l = seq(0, 100, length = 6)))
show_col(col2hcl(reds, alpha = seq(0, 1, length = 6)))