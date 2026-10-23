# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: is_logging_enabled.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 8

suppressPackageStartupMessages(library(otel))
fun <- function() {
  if (otel::is_logging_enabled()) {
    xattr <- calculate_some_extra_attributes()
    otel::log("Starting fun", attributes = xattr)
  }
  # ...
}