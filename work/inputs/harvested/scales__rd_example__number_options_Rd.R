# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: number_options.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 15

suppressPackageStartupMessages(library(scales))
# Default number formatting
x <- c(0.1, 1, 1000)
label_number()(x)

# Now again with new options set
number_options(style_positive = "plus", decimal.mark = ",")
label_number()(x)

# The options are the argument names with a 'scales.'-prefix
options("scales.style_positive")

# Resetting the options to their defaults
number_options()
label_number()(x)