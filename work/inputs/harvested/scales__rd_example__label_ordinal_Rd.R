# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: label_ordinal.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 16

suppressPackageStartupMessages(library(scales))
demo_continuous(c(1, 5))
demo_continuous(c(1, 5), labels = label_ordinal())
demo_continuous(c(1, 5), labels = label_ordinal(rules = ordinal_french()))

# The rules are just a set of regular expressions that are applied in turn
ordinal_french()
ordinal_english()

# Note that ordinal rounds values, so you may need to adjust the breaks too
demo_continuous(c(1, 10))
demo_continuous(c(1, 10), labels = label_ordinal())
demo_continuous(c(1, 10),
  labels = label_ordinal(),
  breaks = breaks_width(2)
)