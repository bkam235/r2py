# r2py crawler metadata
# package: pkgload
# source_type: rd_example
# topic: parse_ns_file.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pkgload\help
# lines: 4

suppressPackageStartupMessages(library(pkgload))
if (has_tests()) {
parse_ns_file(pkgtest("testLoadHooks"))
}