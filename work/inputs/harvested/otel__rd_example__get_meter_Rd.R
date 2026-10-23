# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: get_meter.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 7

suppressPackageStartupMessages(library(otel))
myfun <- function() {
  mtr <- otel::get_meter()
  ctr <- mtr$create_counter("session-count")
  ctr$add(1)
}
myfun()