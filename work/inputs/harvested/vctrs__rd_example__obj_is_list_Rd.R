# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: obj_is_list.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 33

suppressPackageStartupMessages(library(vctrs))
obj_is_list(list())
obj_is_list(list_of(1))
obj_is_list(data.frame())

list_all_vectors(list(1, mtcars))
list_all_vectors(list(1, environment()))

list_all_size(list(1:2, 2:3), 2)
list_all_size(list(1:2, 2:4), 2)

list_all_recyclable(list(1, 2:3), 2)
list_all_recyclable(list(1, 2:4), 2)

# `list_`-prefixed functions assume a list:
try(list_all_vectors(environment()))

# `NULL` elements are not considered vectors and generally have a size of 0
try(list_check_all_vectors(list(1, NULL, 2)))
try(list_check_all_size(list(1, NULL, 2), size = 1))

# However, it is often useful to perform upfront vector/size checks on a
# list, excluding `NULL`s, and then filter them out later on
list_check_all_vectors(list(1, NULL, 2), allow_null = TRUE)
list_check_all_size(list(1, NULL, 2), size = 1, allow_null = TRUE)

# Performing the checks before removing `NULL`s from the list ensures that
# any errors report the correct index. Note how the index is incorrect from a
# user's point of view if we filter out `NULL` too soon.
xs <- list(1, NULL, 2:3)
try(list_check_all_size(xs, size = 1, allow_null = TRUE))
xs <- vec_slice(xs, !vec_detect_missing(xs))
try(list_check_all_size(xs, size = 1))