# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: inherits_any.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 17

suppressPackageStartupMessages(library(rlang))
obj <- structure(list(), class = c("foo", "bar", "baz"))

# With the _any variant only one class must match:
inherits_any(obj, c("foobar", "bazbaz"))
inherits_any(obj, c("foo", "bazbaz"))

# With the _all variant all classes must match:
inherits_all(obj, c("foo", "bazbaz"))
inherits_all(obj, c("foo", "baz"))

# The order of classes must match as well:
inherits_all(obj, c("baz", "foo"))

# inherits_only() checks that the class vectors are identical:
inherits_only(obj, c("foo", "baz"))
inherits_only(obj, c("foo", "bar", "baz"))