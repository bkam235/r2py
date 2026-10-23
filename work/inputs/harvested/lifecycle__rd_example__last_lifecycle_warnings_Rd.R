# r2py crawler metadata
# package: lifecycle
# source_type: rd_example
# topic: last_lifecycle_warnings.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\help
# lines: 18

suppressPackageStartupMessages(library(lifecycle))
# These examples are not run because `last_lifecycle_warnings()` does not
# work well within knitr and pkgdown


f <- function() invisible(g())
g <- function() list(h(), i())
h <- function() deprecate_warn("1.0.0", "this()")
i <- function() deprecate_warn("1.0.0", "that()")
f()

# Print all the warnings that occurred during the last command:
last_lifecycle_warnings()


# By default, the backtraces are printed in their simplified form.
# Use `simplify` to control the verbosity:
print(last_lifecycle_warnings(), simplify = "none")