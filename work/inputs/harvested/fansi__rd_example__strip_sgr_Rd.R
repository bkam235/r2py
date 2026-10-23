# r2py crawler metadata
# package: fansi
# source_type: rd_example
# topic: strip_sgr.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fansi\help
# lines: 4

suppressPackageStartupMessages(library(fansi))
## convenience function, same as `strip_ctl(ctl=c('sgr', 'url'))`
string <- "hello\033k\033[45p world\n\033[31mgoodbye\a moon"
strip_sgr(string)