# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: extract_http_context.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 4

suppressPackageStartupMessages(library(otel))
hdr <- otel::pack_http_context()
ctx <- otel::extract_http_context()
ctx$is_valid()