# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: pal_brewer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 8

suppressPackageStartupMessages(library(scales))
show_col(pal_brewer()(10))
show_col(pal_brewer("div")(5))
show_col(pal_brewer(palette = "Greens")(5))

# Can use with gradient_n to create a continuous gradient
cols <- pal_brewer("div")(5)
show_col(pal_gradient_n(cols)(seq(0, 1, length.out = 30)))