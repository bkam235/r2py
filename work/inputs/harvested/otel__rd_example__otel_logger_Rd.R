# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: otel_logger.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 5

suppressPackageStartupMessages(library(otel))
lp <- get_default_logger_provider()
lgr <- lp$get_logger()
platform <- utils::sessionInfo()$platform
lgr$log("This is a log message from {platform}.", severity = "trace")