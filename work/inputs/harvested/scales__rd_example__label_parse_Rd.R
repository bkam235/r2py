# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: label_parse.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 10

suppressPackageStartupMessages(library(scales))
# Use label_parse() with discrete scales
greek <- c("alpha", "beta", "gamma")
demo_discrete(greek)
demo_discrete(greek, labels = label_parse())

# Use label_math() with continuous scales
demo_continuous(c(1, 5))
demo_continuous(c(1, 5), labels = label_math(alpha[.x]))
demo_continuous(c(1, 5), labels = label_math())