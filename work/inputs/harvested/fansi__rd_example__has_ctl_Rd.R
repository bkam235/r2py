# r2py crawler metadata
# package: fansi
# source_type: rd_example
# topic: has_ctl.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fansi\help
# lines: 5

suppressPackageStartupMessages(library(fansi))
has_ctl("hello world")
has_ctl("hello\nworld")
has_ctl("hello\nworld", "sgr")
has_ctl("hello\033[31mworld\033[m", "sgr")