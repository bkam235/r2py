# r2py crawler metadata
# package: pkgdown
# source_type: rd_example
# topic: test-long-lines.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pkgdown\help
# lines: 7

suppressPackageStartupMessages(library(pkgdown))
pkgdown:::ruler()

cat(rep("x ", 100), sep = "")
cat(rep("xy", 100), sep = "")
cat(rep("x ", 100), sep = "")
cat(rep("xy", 100), sep = "")