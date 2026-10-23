# r2py crawler metadata
# package: diffobj
# source_type: rd_example
# topic: as.character-DiffSummary-method.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\help
# lines: 4

suppressPackageStartupMessages(library(diffobj))
as.character(
  summary(diffChr(letters, letters[-c(5, 15)], format="raw", pager="off"))
)