# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: get_logger.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 6

suppressPackageStartupMessages(library(otel))
myfun <- function() {
  lgr <- otel::get_logger()
  otel::log("Log message", logger = lgr)
}
myfun()