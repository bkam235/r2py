# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: sym.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 26

suppressPackageStartupMessages(library(rlang))
# Create a symbol
sym("cyl")

# Create a list of symbols
syms(c("cyl", "am"))

# Symbolised names refer to variables
eval(sym("cyl"), mtcars)

# Beware of scoping issues
Cyl <- "wrong"
eval(sym("Cyl"), mtcars)

# Data symbols are explicitly scoped in the data mask
try(eval_tidy(data_sym("Cyl"), mtcars))

# These can only be used with tidy eval functions
try(eval(data_sym("Cyl"), mtcars))

# The empty string returns the missing argument:
sym("")

# This way sym() and as_string() are inverse of each other:
as_string(missing_arg())
sym(as_string(missing_arg()))