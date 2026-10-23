# r2py crawler metadata
# package: lifecycle
# source_type: rd_example
# topic: signal_stage.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\help
# lines: 6

suppressPackageStartupMessages(library(lifecycle))
foofy <- function(x, y, z) {
  signal_stage("experimental", "foofy()")
  x + y / z
}
foofy(1, 2, 3)