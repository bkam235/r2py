# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct_count.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 6

suppressPackageStartupMessages(library(forcats))
f <- factor(sample(letters)[rpois(1000, 10)])
table(f)
fct_count(f)
fct_count(f, sort = TRUE)
fct_count(f, sort = TRUE, prop = TRUE)