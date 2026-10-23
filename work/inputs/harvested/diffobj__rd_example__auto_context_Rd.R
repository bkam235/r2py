# r2py crawler metadata
# package: diffobj
# source_type: rd_example
# topic: auto_context.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\help
# lines: 8

suppressPackageStartupMessages(library(diffobj))
## `pager="off"` for CRAN compliance; you may omit in normal use
diffChr(letters, letters[-13], context=auto_context(0, 3), pager="off")
diffChr(letters, letters[-13], context=auto_context(0, 10), pager="off")
diffChr(
  letters, letters[-13], context=auto_context(0, 10), line.limit=3L,
  pager="off"
)