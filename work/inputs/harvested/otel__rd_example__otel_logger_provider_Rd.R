# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: otel_logger_provider.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 4

suppressPackageStartupMessages(library(otel))
lp <- otel::get_default_logger_provider()
lgr <- lp$get_logger()
lgr$is_enabled()