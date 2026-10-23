# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: s3_register.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 10

suppressPackageStartupMessages(library(vctrs))
# A typical use case is to dynamically register tibble/pillar methods
# for your class. That way you avoid creating a hard dependency on packages
# that are not essential, while still providing finer control over
# printing when they are used.

.onLoad <- function(...) {
  s3_register("pillar::pillar_shaft", "vctrs_vctr")
  s3_register("tibble::type_sum", "vctrs_vctr")
}