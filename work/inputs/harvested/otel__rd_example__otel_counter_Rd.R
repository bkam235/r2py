# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: otel_counter.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 5

suppressPackageStartupMessages(library(otel))
mp <- get_default_meter_provider()
mtr <- mp$get_meter()
ctr <- mtr$create_counter("session")
ctr$add(1)