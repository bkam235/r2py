# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: call_args.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 14

suppressPackageStartupMessages(library(rlang))
call <- quote(f(a, b))

# Subsetting a call returns the arguments converted to a language
# object:
call[-1]

# On the other hand, call_args() returns a regular list that is
# often easier to work with:
str(call_args(call))

# When the arguments are unnamed, a vector of empty strings is
# supplied (rather than NULL):
call_args_names(call)