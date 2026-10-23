# r2py crawler metadata
# package: otel
# source_type: rd_example
# topic: otel_span_context.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\otel\help
# lines: 9

suppressPackageStartupMessages(library(otel))
spc <- get_active_span_context()
spc$get_trace_flags()
spc$get_trace_id()
spc$get_span_id()
spc$is_remote()
spc$is_sampled()
spc$is_valid()
spc$to_http_headers()