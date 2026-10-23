# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: end_span.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 24

suppressPackageStartupMessages(library(otel))
fun <- function() {
  # start span, do not activate
  spn <- otel::start_span("myfun")
  # do not leak resources
  on.exit(otel::end_span(spn), add = TRUE)
  myfun <- function() {
     # activate span for this function
     otel::local_active_span(spn)
     # create child span
     spn2 <- otel::start_local_active_span("myfun/2")
  }

  myfun2 <- function() {
    # activate span for this function
    otel::local_active_span(spn)
    # create child span
    spn3 <- otel::start_local_active_span("myfun/3")
  }
  myfun()
  myfun2()
  end_span(spn)
}
fun()