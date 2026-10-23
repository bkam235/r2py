# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: lvls.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 5

suppressPackageStartupMessages(library(forcats))
f <- factor(c("a", "b", "c"))
lvls_reorder(f, 3:1)
lvls_revalue(f, c("apple", "banana", "carrot"))
lvls_expand(f, c("a", "b", "c", "d"))