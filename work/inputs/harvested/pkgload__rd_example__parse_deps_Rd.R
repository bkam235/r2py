# r2py crawler metadata
# package: pkgload
# source_type: rd_example
# topic: parse_deps.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pkgload\help
# lines: 4

suppressPackageStartupMessages(library(pkgload))
parse_deps("httr (< 2.1),\nRCurl (>= 3)")
# only package dependencies are returned
parse_deps("utils (== 2.12.1),\ntools,\nR (>= 2.10),\nmemoise")