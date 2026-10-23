# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: label_wrap.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 9

suppressPackageStartupMessages(library(scales))
x <- c(
  "this is a long label",
  "this is another long label",
  "this a label this is even longer"
)
demo_discrete(x)
demo_discrete(x, labels = label_wrap(10))
demo_discrete(x, labels = label_wrap(20))