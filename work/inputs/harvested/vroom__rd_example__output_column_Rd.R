# r2py crawler metadata
# package: vroom
# source_type: rd_example
# topic: output_column.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vroom\help
# lines: 8

suppressPackageStartupMessages(library(vroom))
# Most types are returned unchanged
output_column(1)
output_column("x")

# datetimes are formatted in ISO 8601
output_column(Sys.Date())
output_column(Sys.time())