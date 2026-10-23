# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: label_bytes.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 17

suppressPackageStartupMessages(library(scales))
demo_continuous(c(1, 1e6))
demo_continuous(c(1, 1e6), labels = label_bytes())

# Auto units are particularly nice on log scales
demo_log10(c(1, 1e7), labels = label_bytes())

# You can also set the units
demo_continuous(c(1, 1e6), labels = label_bytes("kB"))

# You can also use binary units where a megabyte is defined as
# (1024) ^ 2 bytes rather than (1000) ^ 2. You'll need to override
# the default breaks to make this more informative.
demo_continuous(c(1, 1024^2),
  breaks = breaks_width(250 * 1024),
  labels = label_bytes("auto_binary")
)