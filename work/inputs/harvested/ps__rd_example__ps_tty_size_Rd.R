# r2py crawler metadata
# package: ps
# source_type: rd_example
# topic: ps_tty_size.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ps\help
# lines: 8

suppressPackageStartupMessages(library(ps))
# An example that falls back to the 'width' option
tryCatch(
  ps_tty_size(),
  ps_unknown_tty_size = function(err) {
    c(width = getOption("width"), height = NA_integer_)
  }
)