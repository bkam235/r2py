# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct_c.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 11

suppressPackageStartupMessages(library(forcats))
fa <- factor("a")
fb <- factor("b")
fab <- factor(c("a", "b"))

c(fa, fb, fab)
fct_c(fa, fb, fab)

# You can also pass a list of factors with !!!
fs <- list(fa, fb, fab)
fct_c(!!!fs)