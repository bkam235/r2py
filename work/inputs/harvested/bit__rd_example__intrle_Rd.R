# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: intrle.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 11

suppressPackageStartupMessages(library(bit))
intrle(sample(1:10))
  intrle(diff(1:10))
  intisasc(1:10)
  intisasc(10:1)
  intisasc(c(NA, 1:10))
  intisdesc(1:10)
  intisdesc(c(10:1, NA))
  intisdesc(c(10:6, NA, 5:1))
  intisdesc(c(10:6, NA, 5:1), na.method="skip")
  intisdesc(c(10:6, NA, 5:1), na.method="break")