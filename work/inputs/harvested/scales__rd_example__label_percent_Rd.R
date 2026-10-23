# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: label_percent.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 10

suppressPackageStartupMessages(library(scales))
demo_continuous(c(0, 1))
demo_continuous(c(0, 1), labels = label_percent())

# Use prefix and suffix to create your own variants
french_percent <- label_percent(
  decimal.mark = ",",
  suffix = " %"
)
demo_continuous(c(0, .01), labels = french_percent)