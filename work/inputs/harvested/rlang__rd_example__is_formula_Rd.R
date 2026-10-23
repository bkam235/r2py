# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: is_formula.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 33

suppressPackageStartupMessages(library(rlang))
is_formula(~10)
is_formula(10)

# If you don't supply `lhs`, both one-sided and two-sided formulas
# will return `TRUE`
is_formula(disp ~ am)
is_formula(~am)

# You can also specify whether you expect a LHS:
is_formula(disp ~ am, lhs = TRUE)
is_formula(disp ~ am, lhs = FALSE)
is_formula(~am, lhs = TRUE)
is_formula(~am, lhs = FALSE)

# Handling of unevaluated formulas is a bit tricky. These formulas
# are special because they don't inherit from `"formula"` and they
# don't carry an environment (they are not scoped):
f <- quote(~foo)
f_env(f)

# By default unevaluated formulas are treated as formulas
is_formula(f)

# Supply `scoped = TRUE` to ensure you have an evaluated formula
is_formula(f, scoped = TRUE)

# By default unevaluated formulas not treated as bare formulas
is_bare_formula(f)

# If you supply `scoped = TRUE`, they will be considered bare
# formulas even though they don't inherit from `"formula"`
is_bare_formula(f, scoped = TRUE)