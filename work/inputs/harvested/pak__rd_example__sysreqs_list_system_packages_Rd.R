# r2py crawler metadata
# package: pak
# source_type: rd_example
# topic: sysreqs_list_system_packages.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pak\help
# lines: 4

suppressPackageStartupMessages(library(pak))
if (Sys.getenv("IN_PKGDOWN") == "true" && Sys.info()[["sysname"]] == "Linux") (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
sysreqs_list_system_packages()[1:10,]
}) # examplesIf