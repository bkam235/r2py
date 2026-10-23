# r2py crawler metadata
# package: diffobj
# source_type: rd_example
# topic: diffPrint.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\help
# lines: 11

suppressPackageStartupMessages(library(diffobj))
## `pager="off"` for CRAN compliance; you may omit in normal use
old.opt <- options(diffobj.pager='off'); on.exit(old.opt)

diffPrint(letters, letters[-5])

## Change the default banner/title
diffPrint(
  letters, letters[-5],
  tar.banner='COMPLETE', cur.banner='INCOMPLETE'
)