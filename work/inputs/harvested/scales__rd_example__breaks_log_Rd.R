# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: breaks_log.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 14

suppressPackageStartupMessages(library(scales))
demo_log10(c(1, 1e5))
demo_log10(c(1, 1e6))

# Request more breaks by setting n
demo_log10(c(1, 1e6), breaks = breaks_log(6))

# Some tricky ranges
demo_log10(c(2000, 9000))
demo_log10(c(2000, 14000))
demo_log10(c(2000, 85000), expand = c(0, 0))

# An even smaller range that requires falling back to linear breaks
demo_log10(c(1800, 2000))