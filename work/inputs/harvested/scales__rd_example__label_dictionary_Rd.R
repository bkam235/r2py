# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: label_dictionary.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 17

suppressPackageStartupMessages(library(scales))
# Example lookup table
lut <- c(
  "4" = "four wheel drive",
  "r" = "rear wheel drive",
  "f" = "front wheel drive"
)

# Typical usage
demo_discrete(c("4", "r", "f"), labels = label_dictionary(lut))
# By default, extra values ('w') will remain as-is
demo_discrete(c("4", "r", "f", "w"), labels = label_dictionary(lut))
# Alternatively, you can relabel extra values
demo_discrete(
  c("4", "r", "f", "w"),
  labels = label_dictionary(lut, nomatch = "unknown")
)