# r2py crawler metadata
# package: rstudioapi
# source_type: rd_example
# topic: callFun.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rstudioapi\help
# lines: 4

suppressPackageStartupMessages(library(rstudioapi))
if (rstudioapi::isAvailable()) {
  rstudioapi::callFun("versionInfo")
}