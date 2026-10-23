# r2py crawler metadata
# package: pillar
# source_type: rd_example
# topic: format_type_sum.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\help
# lines: 16

suppressPackageStartupMessages(library(pillar))
# Default method: show the type with angle brackets
writeLines(format_type_sum("dbl", width = NULL))
pillar(1)

# AsIs method: show the type without angle brackets
type_sum.accel <- function(x) {
  I("kg m/s^2")
}

# Typically done through NAMESPACE
# (perhaps with an @export directive in roxygen2)
registerS3method("type_sum", "accel", type_sum.accel)

accel <- structure(9.81, class = "accel")
pillar(accel)