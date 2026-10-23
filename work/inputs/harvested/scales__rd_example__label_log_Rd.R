# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: label_log.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 4

suppressPackageStartupMessages(library(scales))
demo_log10(c(1, 1e5), labels = label_log())
demo_log10(c(1, 1e5), breaks = breaks_log(base = 2), labels = label_log(base = 2))
format_log(c(0.1, 1, 10))