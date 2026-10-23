# r2py crawler metadata
# package: fs
# source_type: rd_example
# topic: fs_bytes.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fs\help
# lines: 10

suppressPackageStartupMessages(library(fs))
fs_bytes("1")
fs_bytes("1K")
fs_bytes("1Kb")
fs_bytes("1Kib")
fs_bytes("1MB")

fs_bytes("1KB") < "1MB"

sum(fs_bytes(c("1MB", "5MB", "500KB")))