# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: otel_tracer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 4

suppressPackageStartupMessages(library(otel))
tp <- get_default_tracer_provider()
trc <- tp$get_tracer()
trc$is_enabled()