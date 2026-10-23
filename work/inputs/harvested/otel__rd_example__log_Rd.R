# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: log.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 4

suppressPackageStartupMessages(library(otel))
host <- "my.db.host"
port <- 6667
otel::log("Connecting to database at {host}:{port}")