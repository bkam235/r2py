# r2py crawler metadata
# package: lifecycle
# source_type: rd_example
# topic: deprecate_soft.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lifecycle\help
# lines: 33

suppressPackageStartupMessages(library(lifecycle))
# A deprecated function `foo`:
deprecate_warn("1.0.0", "foo()")

# A deprecated argument `arg`:
deprecate_warn("1.0.0", "foo(arg)")

# A partially deprecated argument `arg`:
deprecate_warn("1.0.0", "foo(arg = 'must be a scalar integer')")

# A deprecated function with a function replacement:
deprecate_warn("1.0.0", "foo()", "bar()")

# A deprecated function with a function replacement from a
# different package:
deprecate_warn("1.0.0", "foo()", "otherpackage::bar()")

# A deprecated function with custom message:
deprecate_warn(
  when = "1.0.0",
  what = "foo()",
  details = "Please use `otherpackage::bar(foo = TRUE)` instead"
)

# A deprecated function with custom bulleted list:
deprecate_warn(
  when = "1.0.0",
  what = "foo()",
  details = c(
    x = "This is dangerous",
    i = "Did you mean `safe_foo()` instead?"
  )
)