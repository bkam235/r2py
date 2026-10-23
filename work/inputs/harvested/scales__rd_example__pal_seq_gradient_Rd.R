# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: pal_seq_gradient.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 6

suppressPackageStartupMessages(library(scales))
x <- seq(0, 1, length.out = 25)
show_col(pal_seq_gradient()(x))
show_col(pal_seq_gradient("white", "black")(x))

show_col(pal_seq_gradient("white", "#90503F")(x))