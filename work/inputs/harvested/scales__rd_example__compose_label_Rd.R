# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: compose_label.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 11

suppressPackageStartupMessages(library(scales))
demo_continuous(
  c(-100, 100),
  labels = compose_label(abs, number, \(x) paste0(x, " foobar"), toupper)
)

# Same result
demo_continuous(
  c(-100, 100),
  labels = compose_label(abs, label_number(suffix = " FOOBAR"))
)