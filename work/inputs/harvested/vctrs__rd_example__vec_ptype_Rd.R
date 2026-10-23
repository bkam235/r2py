# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_ptype.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 56

suppressPackageStartupMessages(library(vctrs))
# Unknown types ------------------------------------------
vec_ptype_show()
vec_ptype_show(NULL)

# Vectors ------------------------------------------------
vec_ptype_show(1:10)
vec_ptype_show(letters)
vec_ptype_show(TRUE)

vec_ptype_show(Sys.Date())
vec_ptype_show(Sys.time())
vec_ptype_show(factor("a"))
vec_ptype_show(ordered("a"))

# Matrices -----------------------------------------------
# The prototype of a matrix includes the number of columns
vec_ptype_show(array(1, dim = c(1, 2)))
vec_ptype_show(array("x", dim = c(1, 2)))

# Data frames --------------------------------------------
# The prototype of a data frame includes the prototype of
# every column
vec_ptype_show(iris)

# The prototype of multiple data frames includes the prototype
# of every column that in any data frame
vec_ptype_show(
  data.frame(x = TRUE),
  data.frame(y = 2),
  data.frame(z = "a")
)

# Finalisation -------------------------------------------

# `vec_ptype()` and `vec_ptype2()` return unfinalised ptypes so that they
# can be coerced to any other type
vec_ptype(NA)
vec_ptype2(NA, NA)

# By default `vec_ptype_common()` finalises so that you can use its result
# directly in other vctrs functions
vec_ptype_common(NA, NA)

# You can opt out of finalisation to make it work like `vec_ptype()` and
# `vec_ptype2()` with `.finalise = FALSE`, but don't forget that you must
# call `vec_ptype_finalise()` manually if you do so!
vec_ptype_common(NA, NA, .finalise = FALSE)
vec_ptype_finalise(vec_ptype_common(NA, NA, .finalise = FALSE))

# This can be useful in rare scenarios, like including a separate `default`
# argument in the ptype computation
xs <- list(NA, NA)
default <- "a"
try(vec_ptype2(vec_ptype_common(!!!xs), default))
vec_ptype2(vec_ptype_common(!!!xs, .finalise = FALSE), default)