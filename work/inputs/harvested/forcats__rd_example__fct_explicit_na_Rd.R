# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct_explicit_na.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 14

suppressPackageStartupMessages(library(forcats))
f1 <- factor(c("a", "a", NA, NA, "a", "b", NA, "c", "a", "c", "b"))
fct_count(f1)
table(f1)
sum(is.na(f1))

# previously
f2 <- fct_explicit_na(f1)
# now
f2 <- fct_na_value_to_level(f1)

fct_count(f2)
table(f2)
sum(is.na(f2))