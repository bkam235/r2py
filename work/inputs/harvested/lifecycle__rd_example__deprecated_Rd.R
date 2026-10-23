# r2py crawler metadata
# package: lifecycle
# source_type: rd_example
# topic: deprecated.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\help
# lines: 17

suppressPackageStartupMessages(library(lifecycle))
foobar_adder <- function(foo, bar, baz = deprecated()) {
  # Check if user has supplied `baz` instead of `bar`
  if (lifecycle::is_present(baz)) {

    # Signal the deprecation to the user
    deprecate_warn("1.0.0", "foo::bar_adder(baz = )", "foo::bar_adder(bar = )")

    # Deal with the deprecated argument for compatibility
    bar <- baz
  }

  foo + bar
}

foobar_adder(1, 2)
foobar_adder(1, baz = 2)