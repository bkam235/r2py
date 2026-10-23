# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct_inorder.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 9

suppressPackageStartupMessages(library(forcats))
f <- factor(c("b", "b", "a", "c", "c", "c"))
f
fct_inorder(f)
fct_infreq(f)

f <- factor(1:3, levels = c("3", "2", "1"))
f
fct_inseq(f)