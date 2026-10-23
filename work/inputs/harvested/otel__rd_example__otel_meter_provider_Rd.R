# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: otel_meter_provider.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 4

suppressPackageStartupMessages(library(otel))
mp <- otel::get_default_meter_provider()
mtr <- mp$get_meter()
mtr$is_enabled()