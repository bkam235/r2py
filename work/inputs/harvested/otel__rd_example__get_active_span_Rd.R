# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: get_active_span.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 7

suppressPackageStartupMessages(library(otel))
fun <- function() {
  otel::start_local_active_span("fun")
  spn <- otel::get_active_span()
  spn$set_attribute("key", "attribute-value")
}
fun()