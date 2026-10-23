# r2py crawler metadata
# package: fansi
# source_type: rd_example
# topic: state_at_end.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fansi\help
# lines: 6

suppressPackageStartupMessages(library(fansi))
x <- c("\033[44mhello", "\033[33mworld")
state_at_end(x)
state_at_end(x, carry=TRUE)
(close <- close_state(state_at_end(x, carry=TRUE), normalize=TRUE))
writeLines(paste0(x, close, " no style"))