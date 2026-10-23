# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: type_of.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 27

suppressPackageStartupMessages(library(rlang))
type_of(10L)

# Quosures are treated as a new base type but not formulas:
type_of(quo(10L))
type_of(~10L)

# Compare to base::typeof():
typeof(quo(10L))

# Strings are treated as a new base type:
type_of(letters)
type_of(letters[[1]])

# This is a bit inconsistent with the core language tenet that data
# types are vectors. However, treating strings as a different
# scalar type is quite helpful for switching on function inputs
# since so many arguments expect strings:
switch_type("foo", character = abort("vector!"), string = "result")

# Special and builtin primitives are both treated as primitives.
# That's because it is often irrelevant which type of primitive an
# input is:
typeof(list)
typeof(`$`)
type_of(list)
type_of(`$`)