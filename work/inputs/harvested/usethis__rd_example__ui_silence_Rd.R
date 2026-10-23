# r2py crawler metadata
# package: usethis
# source_type: rd_example
# topic: ui_silence.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\usethis\help
# lines: 7

suppressPackageStartupMessages(library(usethis))
# compare the messaging you see from this:
browse_github("usethis")
# vs. this:
ui_silence(
  browse_github("usethis")
)