# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct_drop.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 8

suppressPackageStartupMessages(library(forcats))
f <- factor(c("a", "b"), levels = c("a", "b", "c"))
f
fct_drop(f)

# Set only to restrict which levels to drop
fct_drop(f, only = "a")
fct_drop(f, only = "c")