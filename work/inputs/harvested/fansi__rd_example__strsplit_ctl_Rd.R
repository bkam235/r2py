# r2py crawler metadata
# package: fansi
# source_type: rd_example
# topic: strsplit_ctl.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fansi\help
# lines: 7

suppressPackageStartupMessages(library(fansi))
strsplit_ctl("\033[31mhello\033[42m world!", " ")

## Splitting by newlines does not work as they are _Control
## Sequences_, but we can use `ctl` to treat them as ordinary
strsplit_ctl("\033[31mhello\033[42m\nworld!", "\n")
strsplit_ctl("\033[31mhello\033[42m\nworld!", "\n", ctl=c("all", "nl"))