# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct_expand.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 6

suppressPackageStartupMessages(library(forcats))
f <- factor(sample(letters[1:3], 20, replace = TRUE))
f
fct_expand(f, "d", "e", "f")
fct_expand(f, letters[1:6])
fct_expand(f, "Z", after = 0)