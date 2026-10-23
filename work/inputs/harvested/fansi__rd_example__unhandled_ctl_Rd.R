# r2py crawler metadata
# package: fansi
# source_type: rd_example
# topic: unhandled_ctl.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fansi\help
# lines: 6

suppressPackageStartupMessages(library(fansi))
string <- c(
  "\033[41mhello world\033[m", "foo\033[22>m", "\033[999mbar",
  "baz \033[31#3m", "a\033[31k", "hello\033m world"
)
unhandled_ctl(string)