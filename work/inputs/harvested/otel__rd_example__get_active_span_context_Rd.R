# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: get_active_span_context.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 9

suppressPackageStartupMessages(library(otel))
fun <- function() {
  otel::start_local_active_span("fun")
  fun2()
}
fun2 <- function() {
  otel::log("Log message", span_context = otel::get_active_span_context())
}
fun()