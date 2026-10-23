# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: otel_span.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 12

suppressPackageStartupMessages(library(otel))
fn <- function() {
  trc <- otel::get_tracer("myapp")
  spn <- trc$start_span("fn")
  # ...
  spn$set_attribute("key", "value")
  # ...
  on.exit(spn$end(status_code = "error"), add = TRUE)
  # ...
  spn$end(status_code = "ok")
}
fn()