# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: start_local_active_span.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 9

suppressPackageStartupMessages(library(otel))
fn1 <- function() {
  otel::start_local_active_span("fn1")
  fn2()
}
fn2 <- function() {
  otel::start_local_active_span("fn2")
}
fn1()