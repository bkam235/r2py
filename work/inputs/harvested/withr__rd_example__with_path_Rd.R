# r2py crawler metadata
# package: withr
# source_type: rd_example
# topic: with_path.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\withr\help
# lines: 5

suppressPackageStartupMessages(library(withr))
# temporarily modify the system PATH, *prefixing* the current path
with_path(getwd(), Sys.getenv("PATH"))
# temporarily modify the system PATH, *appending* to the current path
with_path(getwd(), Sys.getenv("PATH"), "suffix")