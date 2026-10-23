# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: flatten.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 37

suppressPackageStartupMessages(library(rlang))
x <- replicate(2, sample(4), simplify = FALSE)
x

flatten(x)
flatten_int(x)

# With flatten(), only one level gets removed at a time:
deep <- list(1, list(2, list(3)))
flatten(deep)
flatten(flatten(deep))

# But squash() removes all levels:
squash(deep)
squash_dbl(deep)

# The typed flatten functions remove one level and coerce to an atomic
# vector at the same time:
flatten_dbl(list(1, list(2)))

# Only bare lists are flattened, but you can splice S3 lists
# explicitly:
foo <- set_attrs(list("bar"), class = "foo")
str(flatten(list(1, foo, list(100))))
str(flatten(list(1, splice(foo), list(100))))

# Instead of splicing manually, flatten_if() and squash_if() let
# you specify a predicate function:
is_foo <- function(x) inherits(x, "foo") || is_bare_list(x)
str(flatten_if(list(1, foo, list(100)), is_foo))

# squash_if() does the same with deep lists:
deep_foo <- list(1, list(foo, list(foo, 100)))
str(deep_foo)

str(squash(deep_foo))
str(squash_if(deep_foo, is_foo))