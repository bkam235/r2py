# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: label_pvalue.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 9

suppressPackageStartupMessages(library(scales))
demo_continuous(c(0, 1))
demo_continuous(c(0, 1), labels = label_pvalue())
demo_continuous(c(0, 1), labels = label_pvalue(accuracy = 0.1))
demo_continuous(c(0, 1), labels = label_pvalue(add_p = TRUE))

# Or provide your own prefixes
prefix <- c("p < ", "p = ", "p > ")
demo_continuous(c(0, 1), labels = label_pvalue(prefix = prefix))