# r2py crawler metadata
# package: pak
# source_type: rd_example
# topic: sysreqs_platforms.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pak\help
# lines: 4

suppressPackageStartupMessages(library(pak))
if (Sys.getenv("IN_PKGDOWN") == "true") (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
sysreqs_platforms()
}) # examplesIf