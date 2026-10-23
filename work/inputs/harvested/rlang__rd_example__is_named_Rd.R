# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: is_named.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 32

suppressPackageStartupMessages(library(rlang))
# is_named() is a scalar predicate about the whole vector of names:
is_named(c(a = 1, b = 2))
is_named(c(a = 1, 2))

# Unlike is_named2(), is_named() returns `FALSE` for empty vectors
# that don't have a `names` attribute.
is_named(list())
is_named2(list())

# have_name() is a vectorised predicate
have_name(c(a = 1, b = 2))
have_name(c(a = 1, 2))

# Empty and missing names are treated as invalid:
invalid <- set_names(letters[1:5])
names(invalid)[1] <- ""
names(invalid)[3] <- NA

is_named(invalid)
have_name(invalid)

# A data frame normally has valid, unique names
is_named(mtcars)
have_name(mtcars)

# A matrix usually doesn't because the names are stored in a
# different attribute
mat <- matrix(1:4, 2)
colnames(mat) <- c("a", "b")
is_named(mat)
names(mat)