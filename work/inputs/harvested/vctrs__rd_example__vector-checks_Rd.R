# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vector-checks.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 35

suppressPackageStartupMessages(library(vctrs))
obj_is_vector(1)

# Data frames are vectors
obj_is_vector(data_frame())

# Bare lists are vectors
obj_is_vector(list())

# S3 lists are vectors if they explicitly inherit from `"list"`
x <- structure(list(), class = c("my_list", "list"))
obj_is_list(x)
obj_is_vector(x)

# But if they don't explicitly inherit from `"list"`, they aren't
# automatically considered to be vectors. Instead, vctrs considers this
# to be a scalar object, like a linear model returned from `lm()`.
y <- structure(list(), class = "my_list")
obj_is_list(y)
obj_is_vector(y)

# `obj_check_vector()` throws an informative error if the input
# isn't a vector
try(obj_check_vector(y))

# `vec_check_size()` throws an informative error if the size of the
# input doesn't match `size`
vec_check_size(1:5, size = 5)
try(vec_check_size(1:5, size = 4))

# `vec_check_recyclable()` throws an informative error if the input can't
# recycle to size `size`
vec_check_recyclable(1:5, size = 5)
vec_check_recyclable(1, size = 5)
try(vec_check_recyclable(1:2, size = 5))