# r2py crawler metadata
# package: pak
# source_type: rd_example
# topic: sysreqs_check_installed.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pak\help
# lines: 5

suppressPackageStartupMessages(library(pak))
if (Sys.getenv("IN_PKGDOWN") == "true" && Sys.info()[["sysname"]] == "Linux") (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
# This only works on supported platforms
sysreqs_check_installed()
}) # examplesIf