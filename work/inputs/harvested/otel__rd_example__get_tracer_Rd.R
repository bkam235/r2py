# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: get_tracer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 8

suppressPackageStartupMessages(library(otel))
myfun <- function() {
  trc <- otel::get_tracer()
  spn <- trc$start_span()
  on.exit(otel::end_span(spn), add = TRUE)
  otel::local_active_span(spn, end_on_exit = TRUE)
}
myfun()