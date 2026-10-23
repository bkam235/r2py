# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: f_rhs.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 12

suppressPackageStartupMessages(library(rlang))
f_rhs(~ 1 + 2 + 3)
f_rhs(~ x)
f_rhs(~ "A")
f_rhs(1 ~ 2)

f_lhs(~ y)
f_lhs(x ~ y)

f_env(~ x)
f <- as.formula("y ~ x", env = new.env())
f_env(f)