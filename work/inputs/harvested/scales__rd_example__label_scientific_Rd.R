# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: label_scientific.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 6

suppressPackageStartupMessages(library(scales))
demo_continuous(c(1, 10))
demo_continuous(c(1, 10), labels = label_scientific())
demo_continuous(c(1, 10), labels = label_scientific(digits = 3))

demo_log10(c(1, 1e9))