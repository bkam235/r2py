# r2py crawler metadata
# package: pak
# source_type: rd_example
# topic: sysreqs_db_match.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pak\help
# lines: 7

suppressPackageStartupMessages(library(pak))
if (Sys.getenv("IN_PKGDOWN") == "true") (if (getRversion() >= "3.4") withAutoprint else force)({ # examplesIf
sysreqs_db_match(
  c("Needs libcurl", "Java, libssl"),
  sysreqs_platform = "ubuntu-22.04"
)
}) # examplesIf