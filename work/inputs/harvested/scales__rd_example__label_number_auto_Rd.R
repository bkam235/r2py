# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: label_number_auto.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 14

suppressPackageStartupMessages(library(scales))
# Very small and very large numbers get scientific notation
demo_continuous(c(0, 1e-6), labels = label_number_auto())
demo_continuous(c(0, 1e9), labels = label_number_auto())

# Other ranges get the numbers printed in full
demo_continuous(c(0, 1e-3), labels = label_number_auto())
demo_continuous(c(0, 1), labels = label_number_auto())
demo_continuous(c(0, 1e3), labels = label_number_auto())
demo_continuous(c(0, 1e6), labels = label_number_auto())

# Transformation is applied individually so you get as little
# scientific notation as possible
demo_log10(c(1, 1e7), labels = label_number_auto())