# r2py crawler metadata
# package: zip
# source_type: rd_example
# topic: unzip_process.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\zip\help
# lines: 7

suppressPackageStartupMessages(library(zip))
ex <- system.file("example.zip", package = "zip")
tmp <- tempfile()
up <- unzip_process()$new(ex, exdir = tmp)
up$wait()
up$get_exit_status()
dir(tmp)