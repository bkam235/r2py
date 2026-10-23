# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: bytes-class.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 10

suppressPackageStartupMessages(library(rlang))
parse_bytes("1")
parse_bytes("1K")
parse_bytes("1Kb")
parse_bytes("1KiB")
parse_bytes("1MB")

parse_bytes("1KB") < "1MB"

sum(parse_bytes(c("1MB", "5MB", "500KB")))